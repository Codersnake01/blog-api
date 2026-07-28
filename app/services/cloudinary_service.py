import cloudinary
import cloudinary.uploader

from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


async def upload_image(file_path: str, folder: str = "blog_posts") -> str:
    """Sube una imagen a Cloudinary y devuelve la URL."""
    result = cloudinary.uploader.upload(file_path, folder=folder)
    return result["secure_url"]
