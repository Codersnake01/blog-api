from datetime import datetime

from pydantic import BaseModel

from app.schemas.user import UserResponse


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    is_approved: bool
    created_at: datetime
    author_id: int
    post_id: int

    author: UserResponse | None = None

    model_config = {"from_attributes": True}
