from os import getenv, path

import numpy as np
from PIL import Image

from model import MODEL_IMAGE_HEIGHT, MODEL_IMAGE_WIDTH
from utils.image import (
    image_crop_center,
    image_from_normalized_ndarray,
    image_to_normalized_ndarray,
)
from utils.triton import TritonRemoteModel

MODEL_ENDPOINT = getenv("MODEL_ENDPOINT", "host.docker.internal:8000")
MODEL_PROTOCOL = getenv("MODEL_PROTOCOL", "http")
MODEL_NAME = getenv("MODEL_NAME", "magenta_image_stylization")


def get_remote_model() -> TritonRemoteModel:
    return TritonRemoteModel(MODEL_ENDPOINT, MODEL_NAME, protocol=MODEL_PROTOCOL)


image_base_path = path.abspath(path.join(path.dirname(__file__), "../tests/data/"))

image_content_file = path.join(image_base_path, "image_adelbert_slack.jpg")
image_content_array = image_to_normalized_ndarray(
    image_crop_center(
        Image.open(image_content_file), MODEL_IMAGE_WIDTH, MODEL_IMAGE_HEIGHT
    )
)

image_style_file = path.join(image_base_path, "style_tensor_dog.jpg")
image_style_array = image_to_normalized_ndarray(
    image_crop_center(
        Image.open(image_style_file), MODEL_IMAGE_WIDTH, MODEL_IMAGE_HEIGHT
    )
)

model = get_remote_model()
result = model(placeholder=image_content_array, placeholder_1=image_style_array)
result_image = image_from_normalized_ndarray(np.squeeze(result[0]))
result_image.save(path.join(image_base_path, "../stylized_test.jpg"))
if getenv("LOOP"):
    i = 0
    while True:
        i += 1
        if i % 10 == 0:
            print("Iteration: ", i)
        model(placeholder=image_content_array, placeholder_1=image_style_array)
