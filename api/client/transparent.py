import requests

# curl -X 'POST' \
#  'http://localhost:8050/stylize/' \
#  -H 'accept: application/json' \
#  -H 'Content-Type: multipart/form-data' \
#  -F 'source_image_file=@Source_Golden_Gate.jpg;type=image/jpeg' \
#  -F 'style_image_file=@Style_Kanagawa.jpg;type=image/jpeg'

url = "http://localhost:8050/stylize/"

headers = {
    "accept": "application/json",
    "Content-Type": "multipart/form-data"
}


files = [
    ("source_image_file", ("Source_Adelbert_Slack.jpg", open("../tests/data/Source_Adelbert_Slack.jpg", "rb"), 'image/jpeg')),
    ("style_image_file", ("Style_Kanagawa.jpg", open("../tests/data/Style_Kanagawa.jpg", "rb"), 'image/jpeg')),
]

req = requests.post(url, files=files)
with open('outfile.jpg', 'wb') as f:
    f.write(req.content)

