from io import BytesIO

import numpy as np
from fastapi import FastAPI, UploadFile
from fastapi.responses import Response  # FileResponse, StreamingResponse
from PIL import Image

from utils.image import (
    image_crop_center,
    image_from_normalized_ndarray,
    image_to_normalized_ndarray,
)
from utils.triton import TritonRemoteModel

MODEL_EXPECTED_WIDTH = 256
MODEL_EXPECTED_HEIGHT = 256

app = FastAPI()
model = TritonRemoteModel(
    "host.docker.internal:8000",
    "magenta_arbitrary-image-stylization-v1-256_2.tar",
    protocol="http",
)


@app.post("/stylize/")
async def generate_image(source_image_file: UploadFile, style_image_file: UploadFile):
    source_image = Image.open(source_image_file.file)
    print(source_image.format, source_image.size, source_image.mode)
    source_image_array = image_to_normalized_ndarray(
        image_crop_center(source_image, MODEL_EXPECTED_WIDTH, MODEL_EXPECTED_HEIGHT)
    )

    style_image = Image.open(style_image_file.file)
    print(style_image.format, style_image.size, style_image.mode)
    style_image_array = image_to_normalized_ndarray(
        image_crop_center(style_image, MODEL_EXPECTED_WIDTH, MODEL_EXPECTED_HEIGHT)
    )

    result = model(style_image_array, source_image_array)
    result_image = image_from_normalized_ndarray(np.squeeze(result[0]))

    with BytesIO() as response_stream:
        result_image.save(response_stream, "JPEG")
        return Response(content=response_stream.getvalue(), media_type="image/jpeg")
