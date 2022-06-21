# AI/ML Developer Tutorial

This tutorial is aimed at AI/ML developers and app developers using Transparent AI as an example.

What you'll do in this tutorial:

* Launch the app with `docker-compose`
* Package a model using the `octoml` cli
* Modify work done at the pre and post processing `ppp` api layer
* Redeploy the app (locally) with `docker-compose`

## Overview

The Transparent AI application is structured into the following 3 components

1. Frontend (/frontend) is a [Gradio](https://github.com/gradio-app/gradio) based interface which the user interacts with. It communicates via HTTP requests to the API server below.

2. API (/api) is a [FastAPI](https://fastapi.tiangolo.com/) based server which handles requests from the frontend and performs pre-processing before dispatching them to the ML model server. It receives responses from the model server and is also responsible for doing any necessary post-processing before returning them back to the frontend.

3. ML models optimized for a set of deployment targets via the [OctoML CLI](https://try.octoml.ai/cli/) which also packaged them into a container consisting of the [NVIDIA Triton™ Inference Server](https://github.com/triton-inference-server) for convenient local testing or cloud deployment.

## Local Setup

1. Ensure that your development machine has the dependencies called out in the [README](../README.md).
2. Clone the repository and open a terminal.
3. Execute `just build-model` in the /transparentai folder. This command, defined in the Justfile does the following.
    - Downloads the Image Style Transfer ML model
    - Packages the model into a Triton server container via the OctoML CLI
    - Brings up the container on ports 8000, 8001, 8002
4. Execute `docker-compose up` in the /transparentai folder. This will build the frontend and api server and create a docker-compose environment which includes the model container built in step 3.
5. You should now have a frontend webapp available at `http://localhost:8888`. The api server is directly available at `http://localhost:8050`

## Modify and Redeploy

Let's add a post-processing grayscale step to the image created by our app.
1. Go to utils/image.py and create an `image_to_grayscale` method.
    ```
    def image_to_grayscale(image: Image) -> Image:
        return image.convert("L")
    ```
2. Import this method in api/main.py. Modify line 15 to the following.
    ```
    from utils.image import (
        image_apply_watermark,
        image_crop_center,
        image_from_normalized_ndarray,
        image_to_normalized_ndarray,
        image_to_grayscale,
    )
3. Inspect the `generate_image` method in api/main.py at line 70. This is where we prepare images for the ML model and then post-process the response before relaying it back.
4. Add the following at line 96
    ```
    result_image = image_to_grayscale(result_image)
    ```
5. Build the restart the app via `just compose-up`
6. Verify that the stylized image is now in grayscale

## Notes

If using [Visual Studio Code](https://code.visualstudio.com/) as your development editor, the repository includes settings and a development container configuration.
