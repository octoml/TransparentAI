from typing import Optional, Tuple

import numpy as np
from PIL import Image


def image_crop_center(image: Image, target_width: int, target_height: int) -> Image:
    if image.mode != "RGB":
        image = image.convert("RGB")
    # Extract a center crop
    width, height = image.size
    if width != height:
        square_size = min(width, height)
        left = (width - square_size) / 2
        top = (height - square_size) / 2
        right = (width + square_size) / 2
        bottom = (height + square_size) / 2
        image = image.crop((left, top, right, bottom))
    # Resize after Crop
    if image.width != target_width or image.height != target_height:
        image = image.resize((target_width, target_height))
    return image


def image_to_normalized_ndarray(image: Image) -> np.ndarray:
    arr = np.expand_dims(np.asarray(image) / 255.0, axis=0).astype(np.float32)
    return arr


def image_from_normalized_ndarray(arr: np.ndarray) -> Image:
    arr = np.uint8(arr * 255)
    image = Image.fromarray(arr)
    return image


def image_apply_watermark(
    image: Image, watermark_path: str, watermark_size: Optional[Tuple[int, int]] = None
) -> Image:
    watermark = Image.open(watermark_path, "r").convert("RGBA")
    if watermark_size:
        watermark = watermark.resize(watermark_size)
    src_w, src_h = image.size
    watermark_w, watermark_h = watermark.size
    # place in bottom right corner
    offset = (max(src_w - watermark_w, 0), max(src_h - watermark_h, 0))
    image.paste(watermark, offset, watermark)
    return image
