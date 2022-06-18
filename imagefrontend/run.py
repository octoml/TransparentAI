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

style_images = [
    ["images/examples/style_kanagawa.jpg"],
    ["images/examples/style_tensor_dog.jpg"],
    ["images/examples/style_tensor_dog_crop.jpg"],
    ["images/examples/pineapple.jpg"],
]

# examples = [
#     ["examples/images/pinneaple.jpg", "examples/images/van.jpg"],
#     ["examples/images/pinneaple.jpg","examples/images/mountain.jpg"],
#     ["examples/images/pinneaple.jpg","examples/images/wood_fire.jpg"],
#     ["examples/images/pinneaple.jpg","examples/images/trees.jpg"],


def stylize_webcam(webcam_data, style_image, target):
    webcam_image = Image.fromarray(webcam_data)
    with BytesIO() as webcam_image_file:
        webcam_image.save(webcam_image_file, "JPEG")
        webcam_image_name = f"webcam_{int(time())}"
        return dispatch(
            webcam_image_name, webcam_image_file.getvalue(), style_image, target
        )


def stylize_upload(upload_image, style_image, target):
    return dispatch(upload_image.name, upload_image.file, style_image, target)


def dispatch(src_image_name, src_image_bytes, style_image, target):
    request_files = [
        ("source_image", (src_image_name, src_image_bytes, "image/jpeg")),
        ("style_image", (style_image.name, style_image.file, "image/jpeg")),
    ]
    start_ns = perf_counter_ns()
    req = requests.post(API_URL_STYLIZE, files=request_files, params={"target": target})
    elapsed_ns = perf_counter_ns() - start_ns
    if req.ok:
        out_image = Image.open(BytesIO(req.content))
        elapsed_ms = elapsed_ns / 1000000
        return out_image, f"<h3>Latency: {elapsed_ms:.2f} ms</h3>"
    return None


def query_targets() -> List[str]:
    req = requests.get(API_URL_TARGETS)
    if req.ok:
        return req.json()
    return []


# def create_app(targets: List[str]):
#     header = """
#     <img src="https://www.datocms-assets.com/45680/1655488521-logo_transparent_ai.png" width=200px height=100px align="left">
#     <center><h1>OctoML Style Transfer Demo</h1></center>
#     """
#     gr.Markdown(header)

#     with gr.Column():

#         with gr.Tabs():
#             tab_upload = gr.TabItem("Upload")
#             with tab_upload:
#                 input_upload = gr.Image(label="Image", source="upload", type="file")
#                 input_upload.style(width=512, height=512, rounded=True)
#                 # button_upload = gr.Button("Stylize", variant="primary")

#             tab_webcam = gr.TabItem("WebCam")
#             with tab_webcam:
#                 input_webcam = gr.Image(label="Webcam", source="webcam", streaming=True)
#                 input_webcam.style(width=512, height=512, rounded=True)
#                 # button_webcam = gr.Button("Stylize", variant="primary")

#         with gr.Column():
#             # with gr.Row():
#             input_target = gr.Radio(
#                 choices=targets, value=targets[0], label="Compute Targets"
#             )
#             with gr.Row():
#                 button_upload = gr.Button("Stylize Upload", variant="primary")
#                 # button_webcam = gr.Button("Stylize Webcam", variant="primary")
#                 # with gr.Row():
#                 output_latency = gr.Markdown("<h3>Latency: --.-- ms</h3>")

#         with gr.Group():
#             input_style = gr.Image(
#                 label="Style",
#                 type="file",
#                 interactive=False,
#                 value=style_images[0][0],
#             )
#             input_style.style(width=512, height=512, rounded=True)

#             input_style_dataset = gr.Dataset(
#                 components=[input_style], samples=style_images, type="index"
#             )

#     # with gr.Row():
#     with gr.Row():

#         output_stylized = gr.Image(
#             label="Stylized Output", type="pil", shape=(256, 256)
#         )
#         output_stylized.style(width=512, height=512)

#         # with gr.Column():

#         #     # Space before the first image
#         #     gr.Markdown("<br/>")

#         #     output_stylized = gr.Image(
#         #         label="Stylized Output", type="pil", shape=(256, 256)
#         #     )
#         #     output_stylized.style(width=550, height=550)

#         #     input_target = gr.Radio(choices=targets, value=targets[0], label="Target")

#         #     button_either = gr.Button("Stylize", variant="primary")

#         #     output_textbox = gr.Markdown("<h3>Latency: --.-- ms</h3>")

#         #     footer = '<br/></br/><br/></br/><br/><img src="https://www.datocms-assets.com/45680/1655488516-logo_octoml.png" width=100px align="right">'
#         #     gr.Markdown(footer)

#     def load_example(example_id):
#         processed_example = input_style.preprocess_example(style_images[example_id][0])
#         return processed_example

#     def tab_upload_selected():
#         print("upload selected")

#     def tab_webcam_selected():
#         print("webcam selected")

#     tab_upload.select(tab_upload_selected, inputs=[], outputs=[])
#     tab_webcam.select(tab_webcam_selected, inputs=[], outputs=[])

#     input_style_dataset.click(
#         load_example,
#         inputs=[input_style_dataset],
#         outputs=[input_style],
#         _postprocess=False,
#         queue=False,
#     )

#     # with gr.Row():
#     #     with gr.Column():
#     #         input_target = gr.Radio(choices=targets, value=targets[0], label="Target")

#     #     with gr.Column():
#     #         output_stylized = gr.Image(
#     #             label="Stylized Output", type="pil", shape=(256, 256)
#     #         )
#     #         output_stylized.style(width=512, height=512)

#     button_upload.click(
#         stylize_upload,
#         inputs=[input_upload, input_style, input_target],
#         outputs=[output_stylized, output_latency],
#     )

#     # button_either.click(
#     #     stylize_upload,
#     #     inputs=[input_upload, input_style, input_target],
#     #     outputs=[output_stylized, output_latency],
#     # )

#     # button_webcam.click(
#     #     stylize_webcam,
#     #     inputs=[input_webcam, input_style, input_target],
#     #     outputs=[output_stylized, output_latency],
#     # )

#     # footer = '<br/><img src="https://www.datocms-assets.com/45680/1655488516-logo_octoml.png" width=100px align="center">'
#     # gr.Markdown(footer)

#     # with gr.Row():
#     #     footer = '<br/><img src="https://www.datocms-assets.com/45680/1655488516-logo_octoml.png" width=100px align="center">'
#     #     gr.Markdown(footer)


def create_app(targets: List[str]):
    header = """
    <img src="https://www.datocms-assets.com/45680/1655488521-logo_transparent_ai.png" width=200px height=100px align="left">
    <center><h1>OctoML Style Transfer Demo</h1>And more promo stuff</center>
    """
    gr.Markdown(header)

    with gr.Tabs():
        tab_upload = gr.TabItem("Upload")
        with tab_upload:
            with gr.Row():
                with gr.Column():
                    input_upload = gr.Image(
                        label="Image",
                        source="upload",
                        type="file",
                        value=style_images[0][0],
                    )
                    input_upload.style(width=512, height=512, rounded=True)
                    input_upload_dataset = gr.Dataset(
                        components=[input_upload],
                        samples=style_images,
                        type="index",
                    )

                    input_style = gr.Image(
                        label="Style",
                        type="file",
                        interactive=False,
                        value=style_images[0][0],
                    )
                    input_style.style(width=512, height=512, rounded=True)
                    input_style_dataset = gr.Dataset(
                        components=[input_style],
                        samples=style_images,
                        type="index",
                    )

                with gr.Column():

                    output_stylized = gr.Image(
                        label="Stylized Output", type="pil"  # , shape=(256, 256)
                    )
                    output_stylized.style(width=640, height=640, rounded=True)

                    input_target = gr.Radio(
                        choices=targets, value=targets[0], label="Compute Targets"
                    )

                    with gr.Row():
                        button_upload = gr.Button("Stylize", variant="secondary")

                    output_latency = gr.Markdown("<h3>Latency: --.-- ms</h3>")

                    gr.Markdown("Things about OctoML")
        #             with gr.Row():
        #                 button_upload = gr.Button("Stylize Upload", variant="primary")
        #                 # button_webcam = gr.Button("Stylize Webcam", variant="primary")
        #                 # with gr.Row():
        #                 output_latency = gr.Markdown("<h3>Latency: --.-- ms</h3>")
        # output_stylized.style(width=512, height=512)

        # input_upload.style(width=512, height=512, rounded=True)
        # button_upload = gr.Button("Stylize", variant="primary")

        tab_webcam = gr.TabItem("WebCam")
        with tab_webcam:
            with gr.Row():
                input_webcam = gr.Image(label="Webcam", source="webcam", streaming=True)
                input_webcam.style(width=512, height=512, rounded=True)
                output_stylized1 = gr.Image(
                    label="Stylized Output", type="pil"  # , shape=(256, 256)
                )
                # output_stylized1.style(width=512, height=512)
            # input_webcam.style(width=512, height=512, rounded=True)
            # button_webcam = gr.Button("Stylize", variant="primary")


if __name__ == "__main__":
    print("Sleeping 7 to wait for api, which is waiting for modelserver")
    time.sleep(7)
    gr.close_all()
    try:
        # targets = ["default"]  # query_targets()
        targets = query_targets()

        # # with gr.Tabs():
        # #     with gr.TabItem("WebCam"):
        # #         with gr.Column():
        # #             with gr.Box():
        # #                 input_webcam = gr.Image(
        # #                     label="Webcam",
        # #                     source="webcam",
        # #                     streaming=True,
        # #                     type="file",
        # #                     shape=(512, 512),
        # #                 )
        # #                 input_style = gr.Gallery(style_images, label="Styles")
        # #         with gr.Column():
        # #             output_stylized = gr.Image(
        # #                 label="Stylized Image", type="pil", shape=(256, 256)
        # #             )
        # #             gr.Radio(choices=targets, value=targets[0], label="Target")

        demo = gr.Blocks()
        with demo:
            create_app(targets)

            # with gr.Row():
            #     gr.Image(interactive=True)
            #     gr.Image()
            # with gr.Row():
            #     gr.Textbox(label="Text")
            #     gr.Number(label="Count")
            #     gr.Radio(choices=["One", "Two"])
            # with gr.Row():
            #     with gr.Row():
            #         with gr.Column():
            #             gr.Textbox(label="Text")
            #             gr.Number(label="Count")
            #             gr.Radio(choices=["One", "Two"])
            #         gr.Image()
            #         with gr.Column():
            #             gr.Image(interactive=True)
            #             gr.Image()
            # gr.Image()
            # gr.Textbox(label="Text")
            # gr.Number(label="Count")
            # gr.Radio(choices=["One", "Two"])

            demo.launch(
                server_name="0.0.0.0",
                server_port=8888,
                share=False,
                debug=True,
                prevent_thread_lock=True,
                favicon_path="./images/assets/favicon.ico",
            )

        # gr_inputs = [
        #     gr.Image(label="Input Image", type="file"),
        #     gr.Image(label="Style Image", type="file"),
        # ]
        # if targets:
        #     gr_inputs.append(
        #         gr.Radio(choices=targets, value=targets[0], label="Target")
        #     )

        # gr.Interface(
        #     title="OctoML Style Transfer Demo",
        #     description="My shiny description",
        #     fn=stylize,
        #     inputs=gr_inputs,
        #     outputs=[gr.Image(label="Stylized Image", type="pil", shape=(256, 256))],
        #     examples=examples,
        # ).launch(
        #     server_name="0.0.0.0",
        #     server_port=8888,
        #     share=False,
        #     debug=True,
        #     prevent_thread_lock=True,
        # )
    finally:
        gr.close_all()
