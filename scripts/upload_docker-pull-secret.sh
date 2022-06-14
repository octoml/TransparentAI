#!/bin/bash

# This is an example, you'll need to change it
kubectl create secret docker-registry pull-secret \
--namespace transparentai \
--docker-server=https://gcr.io \
--docker-username=_json_key \
--docker-password="$(cat pull-secret.json)" \
--docker-email="skrum-service-account-gcr-pull@octonaut-skrum.iam.gserviceaccount.com"
