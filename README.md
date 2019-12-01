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

To join the cluster, run the following on all nodes

`sudo kubeadm join k8s-master-1:6443 --token xxx \
    --discovery-token-ca-cert-hash sha256:869cfa9319b3d569ce3e63295fffc1abdf0944b38870a22477e242218cf5ff77`

### Load balancer

Setting up ingress controller is little different on bare metal than deploying on a cloud provider. We will be using [MetalLb](https://metallb.universe.tf/) as a load balancer.

**Install MetalLB**

`kubectl apply -f https://raw.githubusercontent.com/google/metallb/v0.8.3/manifests/metallb.yaml`

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