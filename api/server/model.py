from utils.triton import TritonRemoteModel
import os

MODEL_IMAGE_WIDTH = 256
MODEL_IMAGE_HEIGHT = 256
MODEL_NAME = os.environ.get("MODEL_NAME", "magenta_arbitrary-image-stylization-v1-256_2.tar")
MODEL_ENDPOINT = os.environ.get("MODEL_ENDPOINT", "host.docker.internal:8000")
MODEL_PROTOCOL = "http"


def get_remote_model() -> TritonRemoteModel:
    return TritonRemoteModel(MODEL_ENDPOINT, MODEL_NAME, protocol=MODEL_PROTOCOL)
