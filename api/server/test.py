from os import path

import numpy as np
from PIL import Image

from utils.image import (
    image_crop_center,
    image_from_normalized_ndarray,
    image_to_normalized_ndarray,
)
from utils.triton import TritonRemoteModel

MODEL_EXPECTED_WIDTH = 256
MODEL_EXPECTED_HEIGHT = 256

image_base_path = path.abspath(path.join(path.dirname(__file__), "../tests/data/"))

image_content_file = path.join(image_base_path, "Source_Golden_Gate.jpg")
image_content_array = image_to_normalized_ndarray(
    image_crop_center(
        Image.open(image_content_file), MODEL_EXPECTED_WIDTH, MODEL_EXPECTED_HEIGHT
    )
)

image_style_file = path.join(image_base_path, "Style_Kanagawa.jpg")
image_style_array = image_to_normalized_ndarray(
    image_crop_center(
        Image.open(image_style_file), MODEL_EXPECTED_WIDTH, MODEL_EXPECTED_HEIGHT
    )
)

model = TritonRemoteModel(
    "host.docker.internal:8000",
    "magenta_arbitrary-image-stylization-v1-256_2.tar",
    protocol="http",
)
result = model(image_style_array, image_content_array)
result_image = image_from_normalized_ndarray(np.squeeze(result[0]))
result_image.save("styled.jpg")
