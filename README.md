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


## k8s

Build and push images to a custom repo. (Push can take 5 minutes)


```bash
just imageRegistry=gcr.io/octonaut-skrum docker-build
just imageRegistry=gcr.io/octonaut-skrum push
```

Install with helm

```bash
cd helm
helm install transparentai .

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
