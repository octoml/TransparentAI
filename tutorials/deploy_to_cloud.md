# Deploy To Cloud Tutorial

This tutorial is aimed at operations engineers and developers using Transparent AI as an example.

What you'll do in this tutorial:

* Package a model using the `octoml` cli
* Deploy to kubernetes using helm
* Accelerate the model for specific hardware using the `octoml` cli
* Pin specific accelerated workloads to cloud instances
* Load test the application
* Explore observability options using prometheus and grafana
* Explore caching and batching options in the model container


### Package the model as a container

Now let's use the `octoml` cli to package a model and add that to our app. This gives you experience and dexterity with the `octoml` cli tool for managing your own models. We also have in-depth cli [walkthroughs](https://github.com/octoml/octoml-cli-tutorials/tree/main/tutorials#demos).

Change directory (`cd`) to the directory containing the models.

```bash
cd ../models/tensorflow_models
```

Run download script to pull down the model file:

```bash
wget https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed -O models/tensorflow_models/magenta_arbitrary-image-stylization-v1-256_2.tar.gz
```

Inspect the `octoml.yaml` config file. Note that in many cases you do not need to provide the shapes to the model. Try using `octoml init` on your own model to see it in action.

```bash
cat octoml.yaml
```

```yaml
---
models:
  magenta_image_stylization:
    path: magenta_arbitrary-image-stylization-v1-256_2.tar.gz
    inputs:
      "placeholder:0":
        shape:
          - 1
          - 256
          - 256
          - 3
        dtype: fp32
      "placeholder_1:0":
        shape:
          - 1
          - 256
          - 256
          - 3
        dtype: fp32
    type: tensorflowsavedmodel
```

Now run a package operation!

```bash
octoml package
```

You should see this output:

```
transparentAI/models/tensorflow_models $ octoml package

Packaging and/or deploying requires an initial download
of a 12+ GB base image. Once downloaded, this base image
will be cached by Docker.
  ✅ Models imported
  ✅ Packages generated
  ✅ Docker images assembled
  ✅ Finalized packages

You may now run `octoml deploy` to deploy the built container, or access the
container via `docker images`.
```


```
transparentAI/models/tensorflow_models $ docker image list  magenta_image_stylization-local
REPOSITORY                        TAG       IMAGE ID       CREATED         SIZE
magenta_image_stylization-local   latest    d1a83786bbd6   6 seconds ago   12.4GB
```

> Optional step: You can test local deployment of the container via `octoml deploy`. If you do this be sure to remove it with docker before attempting to start `docker-compose` again.


### Prepare Kubernetes and Helm

Validate that you have a Kubernetes cluster, auth is set up, and you have helm installed.

```
kubectl get pod
helm version
```

To save you time, we are providing pre-accelerated image models for the following hardware types:

```
g4dn.2xlarge
c5n.xlarge
```

To get optimal performance ensure that your cluster has at least one of these instance types.
You can follow instructions [here](https://github.com/octoml/TransparentAI/blob/cloud_tutorial/tutorials/quickstart.md#acceleration) on how to accelerate models for any hardware type supported by `octoml hardware`.


Change directory to the helm chart.

```bash
cd deploy/helm
```

Edit `values.yaml` to use images from quay.io

Replace:

```yaml
imageRegistry: gcr.io/octonaut-skrum
```

with:

```yaml
imageRegistry: quay.io/transparentai
```


Note the nodeselector applied via helm. This is how we control that the workload lands on the hardware it was accelerated for.

```yaml

models:
  style:
    nodeSelector:
      node.kubernetes.io/instance-type: "g4dn.2xlarge"
```

Change `enableExtraModels` to false. This prevents prevents extra copies of the model serving container from coming up with unaccellerated models.

Change:

```yaml
enableExtraModels: true
```

to:


```yaml
enableExtraModels: false
```

### Deploy to Kubernetes using helm

Run helm install

```bash
cd deploy/helm
helm install transparentai . -n transparentai --create-namespace
```

In subsequent runs while adjusting the chart or values use upgrade:

```bash
helm upgrade transparentai . -n transparentai
```

### Inspect Kubernetes installation

Verify all the pods have come up

```bash
kubectl -n transparentai get pod
kubectl -n transparentai get svc
```


### Check on the app

```bash
kubectl -n transparentai port-forward svc/transparentai 8080:80
```

Now you can access the app through the portforward at [http://localhost:8080](http://localhost:8080).


### Monitoring

Verify you have a prometheus installation.


```bash
kubectl get pod -n monitoring
```

> Note: if your prometheus is not installed in the `monitoring` namespace you may need to modify the `PodMonitor` template at `templates/pmp.yaml`.


Now port-forward to grafana


```bash
kubectl -n monitoring port-forward svc/grafana 3000
```

Now you can open the grafana dashboard via [http://localhost:3000](http://localhost:3000).

The default username and password is `admin/admin`. If you installed via the `kube-stack` then the username and password is `admin/prom-operator`. 

You can upload a triton dashboard from the `deploy` directory of this tutorial.






