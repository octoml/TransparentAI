import os
from io import BytesIO

import gradio as gr
import numpy as np
import requests
from PIL import Image

API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = os.getenv("API_PORT", 8050)
STYLE_IMAGE = os.getenv("STYLE_IMAGE", "Style_Kanagawa.jpg")


examples = [
    ["examples/images/mountain.jpg"],
    ["examples/images/pinneaple.jpg"],
    ["examples/images/van.jpg"],
]


def segment(image):
    print("IM SEGMENTING")
    url = "http://{}:{}/stylize/".format(API_HOST, API_PORT)
    print(url)

    headers = {"accept": "application/json", "Content-Type": "multipart/form-data"}
    # files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}

    img = Image.fromarray(image, "RGB")
    byte_io = BytesIO()
    img.save(byte_io, "JPEG")
    # with open('/tmp/poop', 'wb') as f:
    #    f.write(byte_io)
    files = [
        ("source_image", ("imput_from_gradio.jpg", byte_io.getvalue(), "image/jpeg")),
        ("style_image", (STYLE_IMAGE, open(STYLE_IMAGE, "rb"), "image/jpeg")),
    ]

    req = requests.post(url, files=files)
    # with open('outfile.jpg', 'wb') as f:
    #    f.write(req.content)
    print(req.ok)
    out_image = Image.open(BytesIO(req.content))
    return np.array(out_image)


if __name__ == "__main__":
    gr.close_all()
    try:
        gr.Interface(
            fn=segment, inputs="image", outputs="image", examples=examples
        ).launch(
            server_name="0.0.0.0",
            server_port=8888,
            debug=True,
            prevent_thread_lock=True,
        )
    finally:
        gr.close_all()
