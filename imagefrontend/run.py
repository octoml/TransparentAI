from io import BytesIO
from os import getenv
from typing import List

import gradio as gr
import requests
from PIL import Image

API_HOST = getenv("API_HOST", "localhost")
API_PORT = getenv("API_PORT", 8050)
API_URL = f"http://{API_HOST}:{API_PORT}"
API_URL_STYLIZE = API_URL + "/stylize"
API_URL_TARGETS = API_URL + "/targets"

examples = [
    ["examples/images/mountain.jpg", "examples/images/pineapple.jpg"],
    ["examples/images/van.jpg", "examples/images/pineapple.jpg"],
]

style_images = [
    ["examples/images/style_kanagawa.jpg"],
    ["examples/images/style_tensor_dog.jpg"],
    ["examples/images/style_tensor_dog_crop.jpg"],
    ["examples/images/pineapple.jpg"],
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
    gr.close_all()
    try:
        targets = ["default"]  # query_targets()

        # demo = gr.Blocks()
        # with demo:
        #     gr.Markdown("<h1>OctoML Style Transfer Demo<h1>")
        #     input_webcam = gr.Image(
        #         label="Webcam",
        #         source="webcam",
        #         streaming=True,
        #     )
        #     input_webcam.style(width=640, height=480, rounded=True)
        #     # input_style = gr.Gallery(value=style_images, label="Styles")
        #     # input_style = gr.Gallery(style_images, label="Styles")
        #     output_stylized = gr.Image(
        #         label="Stylized Image", type="pil", shape=(256, 256)
        #     )

        #     output_stylized_dataset = gr.Dataset(
        #         components=[output_stylized], samples=style_images, type="index"
        #     )

        #     def load_example(example_id):
        #         processed_example = output_stylized.preprocess_example(
        #             style_images[example_id]
        #         )
        #         return processed_example

        #     output_stylized_dataset.click(
        #         load_example,
        #         inputs=[output_stylized_dataset],
        #         outputs=[output_stylized],
        #         _postprocess=False,
        #         queue=False,
        #     )

        #     input_target = gr.Radio(choices=targets, value=targets[0], label="Target")
        #     input_target.change(
        #         stylize,
        #         inputs=[input_webcam, input_target],
        #         outputs=output_stylized,
        #     )

        #     # examples = Dataset(
        #     #     components=non_state_inputs,
        #     #     samples=self.examples,
        #     #     type="index",
        #     # )

        #     # def load_example(example_id):
        #     #     processed_examples = [
        #     #         component.preprocess_example(sample)
        #     #         for component, sample in zip(
        #     #             self.input_components, self.examples[example_id]
        #     #         )
        #     #     ]
        #     #     if self.cache_examples:
        #     #         processed_examples += load_from_cache(self, example_id)
        #     #     if len(processed_examples) == 1:
        #     #         return processed_examples[0]
        #     #     else:
        #     #         return processed_examples

        #     # examples.click(
        #     #     load_example,
        #     #     inputs=[examples],
        #     #     outputs=non_state_inputs
        #     #     + (self.output_components if self.cache_examples else []),
        #     #     _postprocess=False,
        #     #     queue=False,
        #     # )

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
            gr.Markdown("<h1>OctoML Style Transfer Demo<h1>")
            with gr.Column():
                input_webcam = gr.Image(label="Webcam", source="webcam", streaming=True)
                input_webcam.style(width=512, height=512, rounded=True)

                input_style = gr.Image(
                    label="Style Image", type="file", interactive=False
                )
                input_style.style(width=512, height=512, rounded=True)

                input_style_dataset = gr.Dataset(
                    components=[input_style], samples=style_images, type="index"
                )

                def load_example(example_id):
                    processed_example = input_style.preprocess_example(
                        style_images[example_id][0]
                    )
                    return processed_example

                input_style_dataset.click(
                    load_example,
                    inputs=[input_style_dataset],
                    outputs=[input_style],
                    _postprocess=False,
                    queue=False,
                )

            with gr.Column():
                input_target = gr.Radio(
                    choices=targets, value=targets[0], label="Target"
                )
                output_stylized = gr.Image(
                    label="Stylized Image", type="pil", shape=(256, 256)
                )
                output_stylized.style(width=512, height=512)

                input_target.change(
                    stylize,
                    inputs=[input_webcam, input_target],
                    outputs=output_stylized,
                )

        demo.launch(
            server_name="0.0.0.0",
            server_port=8888,
            share=False,
            debug=True,
            prevent_thread_lock=True,
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
