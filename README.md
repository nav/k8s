# Kubernetes Playground

An exercise to learn Kubernetes cluster deployment on a bare-metal server. This project includes:
 - a simple [FastAPI](https://fastapi.tiangolo.com/) application 
 - a collection of [Ansible](https://www.ansible.com/) script to setup vpc instances
 - a build script to package application into a [Docker](https://docker.com) image
 - a collection of Kubenetes resources as yaml files
    - [MetalLb](https://metallb.universe.tf/)
    - [Ingress-nginx](https://github.com/kubernetes/ingress-nginx)
    - and application specific Deployment, Service, and Ingress


## VM Setup

 - Remove existing machine id from `/etc/machine-id` and recreate a new one using `sudo systemd-machine-id-setup`

## Ansible setup

Once the VMs are ready, run ansible playbook to install Docker and a few other tools.

For me, the following command works:

```shell
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory/development site.yml --ask-become-pass
```

## Kubernetes setup

### Initialize

Run `sudo kubeadm init --pod-network-cidr=10.244.0.0/16` to initialize the control plane and follow the instructions printed after it finishes.

```shell
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Deploy a pod network
`kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/2140ac876ef134e0ed5af15c65e414cf26827915/Documentation/kube-flannel.yml`

To join the cluster, copy the command from the output of above command and run it on all nodes.

`sudo kubeadm join k8s-master-1:6443 --token xxx --discovery-token-ca-cert-hash sha256:xxx`

### Load balancer

Setting up ingress controller is little different on bare metal than deploying on a cloud provider. We will be using [MetalLb](https://metallb.universe.tf/) as a load balancer.

**Install MetalLB**

`kubectl apply -f https://raw.githubusercontent.com/google/metallb/v0.9.3/manifests/metallb.yaml`

**Usage**

To use MetalLB for your application, use a configuration similar to one below:

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 10.1.1.116-10.1.1.120
```

Actuall config is contained in `deploy/kubernetes/loadbalancer.yaml` file.

### Application specific

To deploy application along with necessary LoadBalancer and Ingress-controller run

```shell
kustomize build deploy/kubernetes | kc apply -f -
```


## Helm setup

Helm is a package manager for Kubernetes. To install Helm on MacOS run:

`brew install helm`

You will need to run a few more commands to make it useful.

```shell
helm repo add stable https://kubernetes-charts.storage.googleapis.com
helm repo update
```


### Install Prometheus

``` shell
kubectl create namespace monitorying

helm install -f deploy/kubernetes/prometheus/prometheus.yaml \
  my-prometheus stable/prometheus \
  --namespace monitoring
```

