import logging
import os
import time
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
    image_apply_watermark,
    image_crop_center,
    image_from_normalized_ndarray,
    image_to_normalized_ndarray,
)
from utils.triton import TritonRemoteModel

logger = logging.getLogger(__name__)

CONFIG_FILE = os.getenv("CONFIG_FILE", "../config.yaml")
config = load_config(CONFIG_FILE)
if not config.targets:
    raise RuntimeError("No target models provided")

WATERMARK_SIZE = (25, 25)
WATERMARK = os.getenv("WATERMARK")
if WATERMARK is not None:
    os.stat("assets/" + WATERMARK)


@dataclass(frozen=True)
class TargetModel:
    config: TargetConfig
    model: TritonRemoteModel


# Wait for triton to be running
logger.info("Waiting 10 seconds for model server.")
time.sleep(10)

target_models: Dict[str, TritonRemoteModel] = dict()
for target_name, target_config in config.targets.items():
    target_url = f"{target_config.host}:{target_config.port}"
    try:
        target_model = TritonRemoteModel(
            target_url, target_config.model, protocol=target_config.protocol
        )
    except Exception as e:
        logger.exception(
            f"Unable to connect to target endpoint '{target_name}' at '{target_url}'"
        )
        raise
    target_models[target_name] = target_model


app = FastAPI()


@app.get("/targets/")
def get_targets() -> List[str]:
    return list(target_models.keys())


@app.post("/stylize/")
async def generate_image(
    source_image: UploadFile,
    style_image: UploadFile,
    target: str = None,
):
    model = target_models.get(target) if target else next(iter(target_models.values()))
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
    if WATERMARK:
        result_image = image_apply_watermark(
            result_image, os.path.join("assets/" + WATERMARK), WATERMARK_SIZE
        )

    with BytesIO() as response_stream:
        result_image.save(response_stream, "JPEG")
        return Response(content=response_stream.getvalue(), media_type="image/jpeg")
