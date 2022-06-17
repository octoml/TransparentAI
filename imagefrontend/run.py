from io import BytesIO
from os import getenv
from typing import List

import time
import gradio as gr
import requests
from PIL import Image

API_HOST = getenv("API_HOST", "localhost")
API_PORT = getenv("API_PORT", 8050)
API_URL = f"http://{API_HOST}:{API_PORT}"
API_URL_STYLIZE = API_URL + "/stylize"
API_URL_TARGETS = API_URL + "/targets"

examples = [
    ["examples/images/pinneaple.jpg", "examples/images/van.jpg"],
    ["examples/images/pinneaple.jpg","examples/images/mountain.jpg"],
    ["examples/images/pinneaple.jpg","examples/images/wood_fire.jpg"],
    ["examples/images/pinneaple.jpg","examples/images/trees.jpg"],

]


def stylize(source_image, style_image, target):
    request_files = [
        (
            "source_image",
            (source_image.name, source_image.file, "image/jpeg"),
        ),
        ("style_image", (style_image.name, style_image.file, "image/jpeg")),
    ]
    req = requests.post(API_URL_STYLIZE, files=request_files, params={"target": target})
    if req.ok:
        out_image = Image.open(BytesIO(req.content))
        return out_image
    return None


def query_targets() -> List[str]:
    req = requests.get(API_URL_TARGETS)
    if req.ok:
        return req.json()
    return []


if __name__ == "__main__":
    print("Sleeping 7 to wait for api, which is waiting for modelserver")
    time.sleep(7)
    gr.close_all()
    try:
        gr_inputs = [
            gr.Image(label="Input Image", type="file"),
            gr.Image(label="Style Image", type="file"),
        ]
        targets = query_targets()
        if targets:
            gr_inputs.append(
                gr.Radio(choices=targets, value=targets[0], label="Target")
            )

        gr.Interface(
            title="OctoML Style Transfer Demo",
            description="My shiny description",
            fn=stylize,
            inputs=gr_inputs,
            outputs=[gr.Image(label="Stylized Image", type="pil", shape=(256, 256))],
            examples=examples,
        ).launch(
            server_name="0.0.0.0",
            server_port=8888,
            share=False,
            debug=True,
            prevent_thread_lock=True,
        )
    finally:
        gr.close_all()
