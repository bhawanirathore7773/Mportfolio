"""Upload validation shared across apps — keeps malicious or oversized
files out of the media library. Used by ImageField(validators=[...]) on
Project, Category, BlogPost, Experience CV uploads, etc.
"""
from django.conf import settings
from django.core.exceptions import ValidationError

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_DOCUMENT_EXTENSIONS = {".pdf"}


def validate_image_file(file_obj):
    ext = "." + file_obj.name.rsplit(".", 1)[-1].lower() if "." in file_obj.name else ""
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file type '{ext}'. Please upload a JPG, PNG or WebP image."
        )
    content_type = getattr(file_obj, "content_type", None)
    if content_type and content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError("This file does not look like a valid image.")
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_obj.size > max_bytes:
        raise ValidationError(
            f"Image is too large ({file_obj.size / 1024 / 1024:.1f} MB). "
            f"Maximum allowed size is {settings.MAX_UPLOAD_SIZE_MB} MB."
        )


def validate_cv_file(file_obj):
    ext = "." + file_obj.name.rsplit(".", 1)[-1].lower() if "." in file_obj.name else ""
    if ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError("Please upload your CV as a PDF file.")
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_obj.size > max_bytes:
        raise ValidationError(
            f"File is too large. Maximum allowed size is {settings.MAX_UPLOAD_SIZE_MB} MB."
        )
