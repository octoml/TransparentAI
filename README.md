# TransparentAI

An example application of how to use OctoML to build an application.

### Getting Started

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
cd helm
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
