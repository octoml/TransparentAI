import gradio as gr
import requests


examples = [
["examples/images/mountain.jpg"],
["examples/images/pinneaple.jpg"],
["examples/images/van.jpg"],
]

def segment(image):
    print("IM SEGMENTING")
    r = requests.get("https://google.com")
    print(r.ok)
    pass  # Implement your image segmentation model here...

gr.Interface(fn=segment, inputs="image", outputs="image", examples=examples).launch(server_name="0.0.0.0", server_port=8888)
