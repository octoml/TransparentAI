from os import path, getenv

import numpy as np
from PIL import Image

from model import MODEL_IMAGE_HEIGHT, MODEL_IMAGE_WIDTH, get_remote_model
from utils.image import (
    image_crop_center,
    image_from_normalized_ndarray,
    image_to_normalized_ndarray,
)

image_base_path = path.abspath(path.join(path.dirname(__file__), "../tests/data/"))

image_content_file = path.join(image_base_path, "Source_Golden_Gate.jpg")
image_content_array = image_to_normalized_ndarray(
    image_crop_center(
        Image.open(image_content_file), MODEL_IMAGE_WIDTH, MODEL_IMAGE_HEIGHT
    )
)

image_style_file = path.join(image_base_path, "Style_Kanagawa.jpg")
image_style_array = image_to_normalized_ndarray(
    image_crop_center(
        Image.open(image_style_file), MODEL_IMAGE_WIDTH, MODEL_IMAGE_HEIGHT
    )
)

model = get_remote_model()
result = model(image_style_array, image_content_array)
result_image = image_from_normalized_ndarray(np.squeeze(result[0]))
result_image.save("styled.jpg")
if getenv("LOOP"):
    i = 0
    while True:
        i += 1
        if i % 10 == 0:
            print("Iteration: ", i)
        result = model(image_style_array, image_content_array)
        result_image = image_from_normalized_ndarray(np.squeeze(result[0]))
