from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.models.post import Post
from app.models.tag import Tag
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.core.limiter import limiter

router = APIRouter()

@router.get("/", response_model=list[PostResponse])
async def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    published_only: bool = True,
    category_id: int | None = None,
    tag_id: int | None = None,
    author_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Post).where(Post.is_deleted == False)
    if published_only:
        stmt = stmt.where(Post.is_published == True)
    if category_id:
        stmt = stmt.where(Post.category_id == category_id)
    if author_id:
        stmt = stmt.where(Post.author_id == author_id)
    if tag_id:
        stmt = stmt.join(Post.tags).where(Tag.id == tag_id)
    stmt = (
        stmt
        .options(selectinload(Post.author), selectinload(Post.category), selectinload(Post.tags))
        .offset(skip)
        .limit(limit)
        .order_by(Post.created_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_post(
    request: Request,
    post_in: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    post = Post(
        title=post_in.title,
        content=post_in.content,
        is_published=post_in.is_published,
        author_id=current_user.id,
        category_id=post_in.category_id,
    )
    if post_in.tag_ids:
        result = await db.execute(select(Tag).where(Tag.id.in_(post_in.tag_ids)))
        tags = result.scalars().all()
        post.tags = list(tags)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    # Recargar relaciones para la respuesta
    stmt = select(Post).where(Post.id == post.id).options(
        selectinload(Post.author), selectinload(Post.category), selectinload(Post.tags)
    )
    post_with_rel = (await db.execute(stmt)).scalars().first()
    return post_with_rel

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Post).where(Post.id == post_id, Post.is_deleted == False).options(
        selectinload(Post.author), selectinload(Post.category), selectinload(Post.tags)
    )
    result = await db.execute(stmt)
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Post).where(Post.id == post_id, Post.is_deleted == False))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_data = post_in.model_dump(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)
    for field, value in update_data.items():
        setattr(post, field, value)
    if tag_ids is not None:
        result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
        post.tags = list(result.scalars().all())
    await db.commit()
    await db.refresh(post)
    stmt = select(Post).where(Post.id == post.id).options(
        selectinload(Post.author), selectinload(Post.category), selectinload(Post.tags)
    )
    updated_post = (await db.execute(stmt)).scalars().first()
    return updated_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Post).where(Post.id == post_id, Post.is_deleted == False))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    post.is_deleted = True
    await db.commit()