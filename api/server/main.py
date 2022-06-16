from dataclasses import dataclass
from io import BytesIO
from typing import Dict, List

import numpy as np
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, Response
from PIL import Image

from config import TargetConfig, load_config
from model import MODEL_IMAGE_HEIGHT, MODEL_IMAGE_WIDTH
from utils.image import (
    image_crop_center,
    image_from_normalized_ndarray,
    image_to_normalized_ndarray,
)
from utils.triton import TritonRemoteModel

config = load_config("../config.yaml")


@dataclass(frozen=True)
class TargetModel:
    config: TargetConfig
    model: TritonRemoteModel


target_models: Dict[str, TritonRemoteModel] = dict()
for target_name, target_config in config.targets.items():
    target_url = f"{target_config.host}:{target_config.port}"
    target_model = TritonRemoteModel(
        target_url, target_config.model, protocol=target_config.protocol
    )
    target_models[target_name] = target_model

app = FastAPI()


@app.get("/targets/")
def get_targets() -> List[str]:
    return list(target_models.keys())


@app.post("/stylize/")
async def generate_image(
    source_image: UploadFile,
    style_image: UploadFile,
    target: str = "default",
):
    model = target_models.get(target)
    if not model:
        return JSONResponse(status_code=404, content={"message": "Target not found"})

    source_image = Image.open(source_image.file)
    source_image_array = image_to_normalized_ndarray(
        image_crop_center(source_image, MODEL_IMAGE_WIDTH, MODEL_IMAGE_HEIGHT)
    )

    style_image = Image.open(style_image.file)
    style_image_array = image_to_normalized_ndarray(
        image_crop_center(style_image, MODEL_IMAGE_WIDTH, MODEL_IMAGE_HEIGHT)
    )

    result = model(placeholder=source_image_array, placeholder_1=style_image_array)
    result_image = image_from_normalized_ndarray(np.squeeze(result[0]))

    with BytesIO() as response_stream:
        result_image.save(response_stream, "JPEG")
        return Response(content=response_stream.getvalue(), media_type="image/jpeg")
