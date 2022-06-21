import numpy as np
from PIL import Image


# TODO-gaz verify this
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


def watermark_image(watermark: str, image: Image) -> Image:
    tai_logo = Image.open('assets/' + watermark, 'r').convert('RGBA')
    tai_w, tai_h = tai_logo.size
    w, h = image.size
    offset = (w-tai_w, h-tai_h) # place in bottom right corner
    image.paste(tai_logo, offset, tai_logo)
    return image

