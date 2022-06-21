# AI/ML Developer Tutorial

This tutorial is aimed at AI/ML developers and app developers using Transparent AI as an example.

What you'll do in this tutorial:

* Launch the app with `docker-compose`
* Package a model using the `octoml` cli
* Accelerate the model using `octoml` cli
* Modify pre-processing done at the `app` layer
* Redeploy the app (locally) with `docker-compose`

## Overview

The Transparent AI application is structured into the following 3 components

1. Frontend (/frontend) is a [Gradio](https://github.com/gradio-app/gradio) based interface which the user interacts with. It communicates via HTTP requests to the API server below.

2. API (/api) is a [FastAPI](https://fastapi.tiangolo.com/) based server which handles requests from the frontend and performs pre-processing before dispatching them to the ML model server. It receives responses from the model server and is also responsible for doing any necessary post-processing before returning them back to the frontend.

3. ML models optimized for a set of deployment targets via the [OctoML CLI](https://try.octoml.ai/cli/) which also packaged them into a container consisting of the [NVIDIA Triton™ Inference Server](https://github.com/triton-inference-server) for convenient local testing or cloud deployment.


## Walkthrough

The first step is ensure that your development machine has the dependencies called out in the [README](../README.md).


