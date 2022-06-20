import requests

url = "http://localhost:8050/stylize/"
files = [
    (
        "source_image",
        (
            "image_adelbert_slack.jpg",
            open("../tests/data/image_adelbert_slack.jpg", "rb"),
            "image/jpeg",
        ),
    ),
    (
        "style_image",
        (
            "style_tensor_dog.jpg",
            open("../tests/data/style_tensor_dog.jpg", "rb"),
            "image/jpeg",
        ),
    ),
]
req = requests.post(url, files=files)
with open("../tests/stylized_request.jpg", "wb") as f:
    f.write(req.content)
