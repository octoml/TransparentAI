from dataclasses import dataclass
from io import BytesIO
from typing import Dict, List

import numpy as np
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, Response
from PIL import Image

from config import Endpoint, load_config
from model import MODEL_IMAGE_HEIGHT, MODEL_IMAGE_WIDTH, MODEL_NAME
from utils.image import (
    image_crop_center,
    image_from_normalized_ndarray,
    image_to_normalized_ndarray,
)
from utils.triton import TritonRemoteModel

config = load_config("../config.yaml")


@dataclass(frozen=True)
class ModelEndpoint:
    endpoint: Endpoint
    model: TritonRemoteModel


model_endpoints: Dict[str, ModelEndpoint] = dict()
for endpoint_name, endpoint in config.endpoints.items():
    endpoint_url = f"{endpoint.host}:{endpoint.port}"
    endpoint_model = TritonRemoteModel(
        endpoint_url, MODEL_NAME, protocol=endpoint.protocol
    )
    model_endpoints[endpoint_name] = endpoint_model

app = FastAPI()


@app.get("/endpoints/")
def get_endpoints() -> List[str]:
    return list(model_endpoints.keys())


@app.post("/stylize/")
async def generate_image(
    endpoint: str, source_image_file: UploadFile, style_image_file: UploadFile
):
    model_endpoint = model_endpoints.get(endpoint)
    if not model_endpoint:
        return JSONResponse(status_code=404, content={"message": "Endpoint not found"})

    source_image = Image.open(source_image_file.file)
    print(source_image.format, source_image.size, source_image.mode)
    source_image_array = image_to_normalized_ndarray(
        image_crop_center(source_image, MODEL_IMAGE_WIDTH, MODEL_IMAGE_HEIGHT)
    )

    style_image = Image.open(style_image_file.file)
    print(style_image.format, style_image.size, style_image.mode)
    style_image_array = image_to_normalized_ndarray(
        image_crop_center(style_image, MODEL_IMAGE_WIDTH, MODEL_IMAGE_HEIGHT)
    )

    result = model_endpoint(style_image_array, source_image_array)
    result_image = image_from_normalized_ndarray(np.squeeze(result[0]))

    with BytesIO() as response_stream:
        result_image.save(response_stream, "JPEG")
        return Response(content=response_stream.getvalue(), media_type="image/jpeg")
