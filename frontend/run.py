import time
from io import BytesIO
from os import getenv
from time import perf_counter_ns, time
from typing import List

import gradio as gr
import requests
from PIL import Image

API_HOST = getenv("API_HOST", "localhost")
API_PORT = getenv("API_PORT", 8050)
API_URL = f"http://{API_HOST}:{API_PORT}"
API_URL_STYLIZE = API_URL + "/stylize"
API_URL_TARGETS = API_URL + "/targets"

MARKDOWN_LOGO = """<img src="https://www.datocms-assets.com/45680/1655488521-logo_transparent_ai.png" width=200px height=100px>"""
MARKDOWN_HEADER = """<h1>OctoML Style Transfer Demo</h1>Try the OctoML CLI! <a href="https://try.octoml.ai/cli/">https://try.octoml.ai/cli/</a>"""
MARKDOWN_DETAILS = """Model acceleration provided by the OctoML.ai Machine Learning Deployment Platform.<br/>Instructions to build, accelerate and deploy this app to your laptop or in the cloud are provided in the following tutorials and documentation.<ul><li><a href="https://try.octoml.ai/cli/">https://try.octoml.ai/cli/</a></li><li><a href="https://github.com/octoml/octoml-cli-tutorials">OctoML CLI Tutorials</a></li><li><a href="https://github.com/octoml/TransparentAI">Transparent AI Sample Repo</a></li></ul>"""
MARKDOWN_FOOTER_LOGO = """<img src="https://www.datocms-assets.com/45680/1655488516-logo_octoml.png" width=80px align="right">"""
MARKDOWN_LATENCY_DEFAULT = """<h3>Latency: -- ms</h3>"""

IMAGES_STYLES = [
    ["images/examples/tensor_dog.jpg"],
    ["images/examples/wood_fire.jpg"],
    ["images/examples/mountain.jpg"],
    ["images/examples/trees.jpg"],
]

IMAGES_SAMPLES = [
    ["images/examples/pineapple.jpg"],
    ["images/examples/van.jpg"],
]


def stylize_webcam(webcam_data, style_image, target):
    if webcam_data is None:
        return None, MARKDOWN_LATENCY_DEFAULT
    webcam_image = Image.fromarray(webcam_data)
    with BytesIO() as webcam_image_file:
        webcam_image.save(webcam_image_file, "JPEG")
        webcam_image_name = f"webcam_{int(time.time())}"
        return request_stylize(
            webcam_image_name, webcam_image_file.getvalue(), style_image, target
        )


def stylize_upload(upload_image, style_image, target):
    return request_stylize(upload_image.name, upload_image.file, style_image, target)


def request_stylize(src_image_name, src_image_bytes, style_image, target):
    request_files = [
        ("source_image", (src_image_name, src_image_bytes, "image/jpeg")),
        ("style_image", (style_image.name, style_image.file, "image/jpeg")),
    ]
    start_ns = perf_counter_ns()
    response = requests.post(
        API_URL_STYLIZE, files=request_files, params={"target": target}
    )
    elapsed_ns = perf_counter_ns() - start_ns
    if response.ok:
        out_image = Image.open(BytesIO(response.content))
        elapsed_ms = elapsed_ns / 1000000
        return out_image, f"<h3>Latency: {elapsed_ms:.2f} ms</h3>"
    return None


def request_targets() -> List[str]:
    response = requests.get(API_URL_TARGETS)
    if response.ok:
        return response.json()
    return []


def create_dataset_selector(image_component: gr.Image, image_list: List[str]):
    dataset = gr.Dataset(
        components=[image_component],
        samples=image_list,
        type="index",
    )

    def load_example(example_id):
        processed_example = image_component.preprocess_example(
            image_list[example_id][0]
        )
        return processed_example

    dataset.click(
        load_example,
        inputs=[dataset],
        outputs=[image_component],
        _postprocess=False,
        queue=False,
    )


def create_tab(source_type: str, targets: List[str]):
    with gr.Row():
        with gr.Column():
            input_source: gr.Image = None
            if source_type == "webcam":
                input_source = gr.Image(label="Webcam", source="webcam", streaming=True)
            else:
                input_source = gr.Image(
                    label="Image",
                    source="upload",
                    type="file",
                    # tool="select",
                    # interactive=False,
                    value=IMAGES_SAMPLES[0][0],
                )
                create_dataset_selector(input_source, IMAGES_SAMPLES)

            input_style = gr.Image(
                label="Style",
                type="file",
                # tool="select",
                # interactive=False,
                value=IMAGES_STYLES[0][0],
            )
            create_dataset_selector(input_style, IMAGES_STYLES)

        with gr.Column():
            output_stylized = gr.Image(label="Stylized Output", type="pil")

            input_target = gr.Radio(
                choices=targets, value=targets[0], label="Compute Targets"
            )

            with gr.Row():
                button_upload = gr.Button("Stylize", variant="primary")

            output_latency = gr.Markdown(MARKDOWN_LATENCY_DEFAULT)

            gr.Markdown(MARKDOWN_DETAILS)
            gr.Markdown(MARKDOWN_FOOTER_LOGO)

        button_upload.click(
            stylize_webcam if source_type == "webcam" else stylize_upload,
            inputs=[input_source, input_style, input_target],
            outputs=[output_stylized, output_latency],
        )


def create_demo(targets: List[str]):

    with gr.Row():
        gr.Markdown(MARKDOWN_LOGO)
        gr.Markdown("     ")
        gr.Markdown(MARKDOWN_HEADER)

    with gr.Tabs():
        with gr.TabItem("Upload Image"):
            create_tab("upload", targets)
        with gr.TabItem("Webcam Image"):
            create_tab("webcam", targets)


if __name__ == "__main__":

    print("Sleeping 7 to wait for api, which is waiting for modelserver")
    import time

    time.sleep(7)

    try:
        targets = request_targets()

        demo = gr.Blocks()
        with demo:
            create_demo(targets)

        demo.launch(
            server_name="0.0.0.0",
            server_port=8888,
            share=False,
            debug=True,
            prevent_thread_lock=True,
            favicon_path="./images/assets/octoml_favicon.png",
        )

    finally:
        gr.close_all()
