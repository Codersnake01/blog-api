from datetime import datetime

from pydantic import BaseModel

from app.schemas.category import CategoryResponse
from app.schemas.tag import TagResponse
from app.schemas.user import UserResponse


class PostCreate(BaseModel):
    title: str
    content: str
    is_published: bool = False
    category_id: int | None = None
    tag_ids: list[int] = []


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_published: bool | None = None
    category_id: int | None = None
    tag_ids: list[int] | None = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    author_id: int
    category_id: int | None = None
    cover_image: str | None = None

    author: UserResponse | None = None
    category: CategoryResponse | None = None
    tags: list[TagResponse] = []

    model_config = {"from_attributes": True}
