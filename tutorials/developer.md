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

2. API (/api) is a FastAPI based server which handles requests from the frontend and performs pre-processing before dispatching them to the ML model server. It is also responsible for doing post-processing for responses received from the model server



Install [Just](https://github.com/casey/just) (I (Jared) refuse to use Make).

To get up and running:

```
just docker-build
```

After that you can run:

```
just compose-up
```
to launch the local development flow.

To launch the OctoML model locally:

```
octoml deploy
```


# OctoML Packaging

How to package

We have the following structure:

```
/models
  /tensorflow_models
    /style_model.tar.gz
    /octoml.yaml
    /accelerated
      /octoml.yaml
  /onnx_models
    /gpt_model.onnx
    /octoml.yaml
    /accelerated
      /octoml.yaml
```

For local pacakging for the model you can `cd` to e.g.
`models/onnx_models` and run `octoml package`.


To do full acceleration with hardware `cd` to
`models/onnx_models/acceleration` and run `octoml package -a.`

For express packaging(much faster) do the same as full but use `octoml package -e`


## k8s

Build and push images to a custom repo. (Push can take 5 minutes)


```bash
just imageRegistry=gcr.io/octonaut-skrum docker-build
just imageRegistry=gcr.io/octonaut-skrum push
```

Setup k8s

```
kubectl create ns transparentai
./scripts/upload_docker-pull-secret.sh
```

Install with helm

```bash
cd deploy/helm
helm install transparentai . -n transparentai

```

Verify pods are running:

```bash
kubectl get pod

transparentai-chat-58dcdccfbf-fn224            1/1     Running             0          101s
transparentai-gpt2-6f65bdf4d7-jms66            1/1     Running             0          101s
transparentai-taiapi-85d96c4b8d-8jnmt          1/1     Running             1          101s
```

Port forward svc

```bash
kubectl port-forward svc/transparentai 8080:80
```

Open browser to [http://localhost:8080](http://localhost:8080)
