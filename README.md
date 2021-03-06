# Transparent AI

Transparent AI is an example project which demonstrates the use of the OctoML CLI to build a cloud ML application.
The CLI can be dowloaded at [https://try.octoml.ai/cli/](https://try.octoml.ai/cli/) and additional CLI specific tutorials are available [here](https://github.com/octoml/octoml-cli-tutorials).

## Quickstart & Tutorials

We've built out several tutorials using this application as a base:

| Name | Audience | Time | Contents |
|--------------|-----------|------------|-|
| [QuickStart](tutorials/quickstart.md) | Everyone | 5 Minutes | Quickstart |
| [Developer](tutorials/developer.md) | AI/ML Developers | 30 Minutes | Pre/Post Processing, Packaging, Acceleration |
| [Deploy to Cloud](tutorials/deploy_to_cloud.md) | Operations | 30 Minutes | Cloud, Observability, Packaging, Acceleration |

## Dependencies


The Transparent AI demo uses [Just](https://github.com/casey/just) to build
the application containers and launch deployments. It also requires the
[`octoml`](https://try.octoml.ai/cli/) command line interface tool that's
used for packaging, accelerating, and managing models.