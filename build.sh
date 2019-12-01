#!/usr/bin/env bash

docker build --force-rm --tag navi/helloworld:latest --file deploy/docker/Dockerfile .
docker push navi/helloworld:latest

