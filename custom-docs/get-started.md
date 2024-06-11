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
