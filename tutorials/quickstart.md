# Quickstart

Get up and running with Transparent AI in five minutes or less!

To get started, make sure you have `docker`, `docker-compose`, and the `octoml` cli tool installed. You can install the cli [here](https://try.octoml.ai/cli/).

### Verify installation

Test that the cli is installed and accept the TOS if needed.

```bash
octoml -V
```

### Clone the repo

```bash
git clone https://github.com/octoml/transparentai
cd transparentai/tutorials
```

### Bring up the app

First, bring up the application using `docker-compose`. Note the `-f` flag here.

> Note: If you are on an M1 Mac the docker image for the `style` container image needs to be changed to run on arm. Use `quay.io/transparentai/noaccel-magenta_image_stylization-mac_m1` instead. This image is designed for M1 Mac use. Rosetta isn't enough in this case.


```bash
transparentai/tutorials $ docker-compose -f quickstart-compose.yaml up
<snip>

                                                                     |
tutorials-style-1     | | strict_readiness                 | 1                                                                                                                                                                                            |
tutorials-style-1     | | exit_timeout                     | 30                                                                                                                                                                                           |
tutorials-style-1     | +----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
tutorials-style-1     | 
tutorials-style-1     | I0621 05:56:17.175235 1 grpc_server.cc:4375] Started GRPCInferenceService at 0.0.0.0:8001
tutorials-style-1     | I0621 05:56:17.175433 1 http_server.cc:3075] Started HTTPService at 0.0.0.0:8000
tutorials-style-1     | I0621 05:56:17.216947 1 http_server.cc:178] Started Metrics Service at 0.0.0.0:8002
tutorials-frontend-1  | Sleeping 7 to wait for api, which is waiting for modelserver
tutorials-api-1       | INFO:     Started server process [7]
tutorials-api-1       | INFO:     Waiting for application startup.
tutorials-api-1       | INFO:     Application startup complete.
tutorials-api-1       | INFO:     Uvicorn running on http://0.0.0.0:8050 (Press CTRL+C to quit)
tutorials-api-1       | INFO:     172.24.0.4:33434 - "GET /targets HTTP/1.1" 307 Temporary Redirect
tutorials-api-1       | INFO:     172.24.0.4:33434 - "GET /targets/ HTTP/1.1" 200 OK
tutorials-frontend-1  | Running on local URL:  http://localhost:8888/
tutorials-frontend-1  | 
tutorials-frontend-1  | To create a public link, set `share=True` in `launch()`.
tutorials-api-1       | INFO:     172.24.0.4:46714 - "POST /stylize?target=cpu HTTP/1.1" 307 Temporary Redirect
tutorials-api-1       | INFO:     172.24.0.4:46714 - "POST /stylize/?target=cpu HTTP/1.1" 200 OK
```

> Note: If you are on an M1 Mac the docker image for the `style` container image needs to be changed to run on arm. Use `quay.io/transparentai/noaccel-magenta_image_stylization-mac_m1` instead. This image is designed for M1 Mac use. Rosetta isn't enough in this case.

You can then navigate to [http://localhost:8888](http://localhost:8888) to use the application.



### Bring it down

Clean up at any time by pressing `ctrl-c` or running:

```bash
transparentAI/tutorials $ docker-compose -f quickstart-compose.yaml down
[+] Running 4/4
 ⠿ Container tutorials-frontend-1  Removed                                                                                                                                      0.0s
 ⠿ Container tutorials-api-1       Removed                                                                                                                                      0.0s
 ⠿ Container tutorials-style-1     Removed                                                                                                                                      0.0s
 ⠿ Network tutorials_default       Removed
```

### Repackage the model as a container

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

> Optional step: You can test local deployment of the container via `octoml deploy`. If you do this be sure to remove it with docker before attempting to start `docker-compose` agian.


### Change out remote model for local model in docker-compose


Next we'll change out the image in the model serving layer of docker-compose with our newly packaged image.

To do this you need to edit one line in `quickstart-compose.yaml`

Where it says:

```yaml
  style: # Model runtime containerized by OctoML CLI into a NVIDIA Triton™ Inference Server
    image: quay.io/transparentai/style-cpu-unaccelerated
```

Change this to refer to your local model:

```yaml
  style: # Model runtime containerized by OctoML CLI into a NVIDIA Triton™ Inference Server
    image: magenta_image_stylization-local
```

Now you can re-launch the app:

```bash
docker-compose -f quickstart-compose.yaml up
```

You can then again navigate to [http://localhost:8888](http://localhost:8888) to use the application.


### Going further

Your newly packaged container has many cool features. To explore them try the following commands out (requires `curl` and `jq`)

```bash
curl -s -X POST localhost:8000/v2/repository/index | jq '.'

curl localhost:8000/v2/models/magenta_image_stylization/config  | jq '.'

curl localhost:8000/v2/models/magenta_image_stylization/stats  | jq '.'
```

### Acceleration

You can accellerate the model for whatever hardware targets you specify.

To do this `cd` to the `acceleration` directory.

```bash
cd models/tensorflow_models/acceleration
```

Review the `octoml.yaml` which specifies the hardware types to accelerate for:

```bash
cat octoml.yaml
```

```yaml
---
models:
  magenta_image_stylization:
    path: ../magenta_arbitrary-image-stylization-v1-256_2.tar.gz
    hardware:
      - aws_c5n.xlarge
      - aws_c5.12xlarge
      - aws_m6g.xlarge
      - aws_g4dn.xlarge
      - skylake_8
      - jetson_agx #(NVIDIA Jetson (OctoML Jetson AGX Xavier))
        #- aws_m6g.16xlarge
        #- aws_m6g.12xlarge
        #- aws_m6g.8xlarge
        #- aws_t4g.2xlarge
        #- rasp4b
        #- jetson_nano #(NVIDIA Jetson (OctoML Jetson Nano))
        #- jetson_nx #(NVIDIA Jetson (OctoML Jetson Xavier NX))
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

> Note: `octoml hardware` (requires api access) will show you a complete list of hardware supported in the platform.

You can run an express acceleration with this command. If you don't have api access yet, you can skip this step. We have provided pre-accelerated images for this model at our [docker registry](https://quay.io/user/transparentai).

```bash
octoml package -e
```
```
models/tensorflow_models/accelerated $ octoml package -e

Packaging and/or deploying requires an initial download
of a 12+ GB base image. Once downloaded, this base image
will be cached by Docker.
  ✅ Models imported
  ✅ Packages generated
Encountered 2 errors in service packaging. Best result may be an unaccelerated package.
  ✅ Docker images assembled
  ✅ Finalized packages
+---------------------------+-----------------+-----------------+--------------------------------------------------+
|           model           |    hardware     | latency_mean_ms |                 output_file_path                 |
+---------------------------+-----------------+-----------------+--------------------------------------------------+
| magenta_image_stylization | aws_c5n.xlarge  |    333.6004     | magenta_image_stylization-aws_c5n.xlarge.tar.gz  |
+---------------------------+-----------------+-----------------+--------------------------------------------------+
| magenta_image_stylization | aws_m6g.xlarge  |    684.4954     | magenta_image_stylization-aws_m6g.xlarge.tar.gz  |
+---------------------------+-----------------+-----------------+--------------------------------------------------+
| magenta_image_stylization | aws_g4dn.xlarge |    29.628025    | magenta_image_stylization-aws_g4dn.xlarge.tar.gz |
+---------------------------+-----------------+-----------------+--------------------------------------------------+
| magenta_image_stylization |    skylake_8    |    228.04054    |    magenta_image_stylization-skylake_8.tar.gz    |
+---------------------------+-----------------+-----------------+--------------------------------------------------+
| magenta_image_stylization | aws_c5.12xlarge |    50.312008    | magenta_image_stylization-aws_c5.12xlarge.tar.gz |
+---------------------------+-----------------+-----------------+--------------------------------------------------+
| magenta_image_stylization |   jetson_agx    |    228.02826    |   magenta_image_stylization-jetson_agx.tar.gz    |
+---------------------------+-----------------+-----------------+--------------------------------------------------+
📦 magenta_image_stylization at: "magenta_image_stylization-aws_c5n.xlarge.tar.gz"
📦 magenta_image_stylization at: "magenta_image_stylization-aws_m6g.xlarge.tar.gz"
📦 magenta_image_stylization at: "magenta_image_stylization-aws_g4dn.xlarge.tar.gz"
📦 magenta_image_stylization at: "magenta_image_stylization-skylake_8.tar.gz"
📦 magenta_image_stylization at: "magenta_image_stylization-aws_c5.12xlarge.tar.gz"
📦 magenta_image_stylization at: "magenta_image_stylization-jetson_agx.tar.gz"


You can now push the local container to a remote container repository (e.g. ECR)
per the instructions in our tutorials repo
(https://github.com/octoml/octoml-cli-tutorials/tree/main/tutorials#kubernetes-deployment),
then run inferences against the container on a remote machine with an
architecture matching the one you've accelerated the model for.

If you wish to locally deploy and test inferences against the accelerated
container, you may run octoml deploy -e or octoml deploy -a, but note that it
only works if the local machine on which you're running the CLI has the same
hardware architecture as the hardware you accelerated the model for (e.g. if you
are running the CLI on an M1 mac, you can only run deployment on your local mac
successfully if you accelerated your model on a Graviton instance, as both of
them share the ARM64 architecture). 
```

Review the images created:

```
models/tensorflow_models/accelerated $ docker images
REPOSITORY                                                                  TAG                                        IMAGE ID       CREATED              SIZE
magenta_image_stylization-jetson_agx                                        latest                                     cdde122bf3d4   18 seconds ago       6.2GB
magenta_image_stylization-aws_c5.12xlarge                                   latest                                     6059ca0b7261   28 seconds ago       678MB
magenta_image_stylization-skylake_8                                         latest                                     6bfc7fd25734   38 seconds ago       678MB
magenta_image_stylization-aws_g4dn.xlarge                                   latest                                     4506a71c05dd   49 seconds ago       8.82GB
magenta_image_stylization-aws_m6g.xlarge                                    latest                                     4417c8a4594c   57 seconds ago       610MB
magenta_image_stylization-aws_c5n.xlarge                                    latest                                     32908317a368   About a minute ago   678MB
```

You can now use these images to deploy accelerated and minimized versions of this application to whatever targets you like.

### Finished!

Great work. Hungry for more? Check out our [developer](developer.md) or [cloud](deploy_to_cloud.md) tutorials or more resources on our [site](https://try.octoml.ai/cli) or our tutorials [specific to the cli](https://github.com/octoml/octoml-cli-tutorials/tree/main/tutorials#demos).
