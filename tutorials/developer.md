# AI/ML Developer Tutorial

This tutorial is aimed at AI/ML developers and app developers using Transparent AI as an example.

What you'll do in this tutorial:

* Launch the app with `docker-compose`
* Package a model using the `octoml` cli
* Modify pre-processing done at the `app` layer
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



