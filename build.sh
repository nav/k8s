#!/usr/bin/env bash

docker build --force-rm --tag navi/helloworld:latest --file build/Dockerfile .
docker push nav/helloworld:latest

