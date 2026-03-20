"""
Upload a local image file to Meta Ad Images and return the image hash.

Meta limits: JPG or PNG, min 600x314px, max 30MB.
The hash is required by create_ad_creative.py.
"""

import os
from PIL import Image
from facebook_business.adobjects.adimage import AdImage
from meta.client import account

MIN_WIDTH = 600
MIN_HEIGHT = 314
MAX_FILE_SIZE_MB = 30


def upload_image(image_path: str) -> str:
    """
    Validate and upload an image to Meta. Returns the image hash string.

    Raises:
        FileNotFoundError: if the file does not exist
        ValueError: if the image fails pre-flight validation
        facebook_business.exceptions.FacebookRequestError: on API failure
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # File size check
    size_mb = os.path.getsize(image_path) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(
            f"Image is {size_mb:.1f}MB — Meta's limit is {MAX_FILE_SIZE_MB}MB. "
            "Please compress the image before uploading."
        )

    # Format and dimension check
    with Image.open(image_path) as img:
        fmt = img.format
        if fmt not in ("JPEG", "PNG"):
            raise ValueError(
                f"Image format '{fmt}' is not supported. Use JPG or PNG."
            )
        width, height = img.size
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            raise ValueError(
                f"Image dimensions {width}x{height}px are too small. "
                f"Minimum required: {MIN_WIDTH}x{MIN_HEIGHT}px."
            )

    # Upload to Meta
    image = account.create_ad_image(
        fields=[],
        params={"filename": image_path},
    )

    image_hash = image.get_hash()
    if not image_hash:
        raise RuntimeError("Meta API returned an image object with no hash.")

    return image_hash
