# This is a simplified get started docs after already upping the tea store (for more specific docs please refer to the standard docs under the root-dir)

## 1. Loadgenerator

- Build image running from root

```sh
docker build -t services/loadgenerator:latest .
```

- Push into docker registry

```sh
docker push loadgenerator:latest
```

- Apply pod config

```sh
apiVersion: v1
kind: Pod
metadata:
  name: loadgenerator
spec:
  containers:
  - name: loadgenerator
    image: loadgenerator:latest
    env:
    - name: FRONTEND_ADDR
      value: "frontend-service" # Der Name des Frontend-Services in Ihrem Cluster
    - name: USERS
      value: "10"
```

```sh
kubectl apply -f loadgenerator/loadgenerator-pod.yaml
```

- apply service to be able to visit web-ui

```sh
kubectl apply -f loadgenerator/loadgenerator-service.yaml
```


## 2. Monitoring

- Create new monitoring namespace to keep default namespace clean

```sh
kubectl create namespace monitoring
```

### a. Grafana

- Create config map

```sh
kubectl create -f grafana/grafana-datasource-config.yaml
```

- Create the deployment/pod

```sh
  kubectl create -f grafana/deployment.yaml -n monitoring
```

- Create the service

```sh
  kubectl create -f grafana/service.yaml -n monitoring
```


### b. Prometheus

- create cluster role

```sh
kubectl create -f prometheus/clusterRole.yaml
```

- run config map

```sh
kubectl create -f prometheus/config-map.yaml
```

- create deployment and service 

```sh
kubectl get pods --namespace=monitoring
```

```sh
kubectl create -f prometheus-service.yaml --namespace=monitoring
```

- configurate the kube-state metrics according to the base docs in the root folder 