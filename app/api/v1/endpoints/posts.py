from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.models.post import Post
from app.models.tag import Tag
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.api.deps import get_current_user
from app.models.user import User
from fastapi import Form, UploadFile, File
import tempfile
import os
from app.services.cloudinary_service import upload_image

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
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    is_published: bool = Form(False),
    category_id: int | None = Form(None),
    tag_ids: str = Form(""),  # IDs separados por comas
    cover_image_file: UploadFile | None = File(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    post_data = {
        "title": title,
        "content": content,
        "is_published": is_published,
        "author_id": current_user.id,
        "category_id": category_id,
    }
    # Subir imagen si existe
    if cover_image_file and cover_image_file.filename:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(cover_image_file.filename)[1]) as tmp:
            content_bytes = await cover_image_file.read()
            tmp.write(content_bytes)
            tmp_path = tmp.name
        try:
            cover_url = await upload_image(tmp_path)
            post_data["cover_image"] = cover_url
        finally:
            os.unlink(tmp_path)

    post = Post(**post_data)
    if tag_ids:
        ids = [int(t) for t in tag_ids.split(",") if t.isdigit()]
        result = await db.execute(select(Tag).where(Tag.id.in_(ids)))
        post.tags = list(result.scalars().all())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    # Recargar relaciones
    stmt = select(Post).where(Post.id == post.id).options(selectinload(Post.author), selectinload(Post.category), selectinload(Post.tags))
    post_with_rel = (await db.execute(stmt)).scalars().first()
    return post_with_rel



@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Post)
        .where(Post.id == post_id, Post.is_deleted == False)
        .options(selectinload(Post.author), selectinload(Post.category), selectinload(Post.tags))
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
        tags = result.scalars().all()
        post.tags = list(tags)

    await db.commit()
    await db.refresh(post)

    # Recargar relaciones para la respuesta
    stmt = (
        select(Post)
        .where(Post.id == post.id)
        .options(selectinload(Post.author), selectinload(Post.category), selectinload(Post.tags))
    )
    result = await db.execute(stmt)
    return result.scalars().first()


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