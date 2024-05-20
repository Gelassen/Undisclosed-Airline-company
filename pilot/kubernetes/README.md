1. There no more way to point out ```Dockerfile``` in ```kubernetes```, now images should be pre-built and pushed to either in  Docker Hub, Google Container Registry (GCR), Amazon Elastic Container Registry (ECR) or Private Docker Register hosted within organization.
2. Secrets are now stored differently, in ```etcd```. ```.env``` could be used to generate ```etcd``` secrets, reference to them later should be applied to kubernetes config file (e.g. services and deployments)   

### Check the status of kubernetes
```
kubectl get deployments -n kafka-pipeline
kubectl get pods -n kafka-pipeline
```

### Setting up cluster
```
url -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64  
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start
```

### Run registry container
```
docker run -d -p 5000:5000 --restart=always --name registry registry:2
```

### Tag your image to point to your registry and push images to Private Registry 
```
docker tag yourusername/kafka-producer:latest localhost:5000/kafka-producer:latest
docker push localhost:5000/kafka-producer:latest
```

### Use the Private Registry in Kubernetes
```
# kafka-producer-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-producer
  namespace: kafka-pipeline
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka-producer
  template:
    metadata:
      labels:
        app: kafka-producer
    spec:
      containers:
      - name: kafka-producer
        image: localhost:5000/kafka-producer:latest  # Use your private registry image
        env:
        - name: KAFKA_BROKER
          value: "kafka:9092"

```

### Deploy the Private Registry on Kubernetes (Optional)

If you prefer to deploy the private registry within your Kubernetes cluster, you can create a deployment and service for it.
Registry Deployment and Service

```
yaml

# registry-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: registry
  namespace: kafka-pipeline
spec:
  replicas: 1
  selector:
    matchLabels:
      app: registry
  template:
    metadata:
      labels:
        app: registry
    spec:
      containers:
      - name: registry
        image: registry:2
        ports:
        - containerPort: 5000

---
# registry-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: registry
  namespace: kafka-pipeline
spec:
  ports:
  - port: 5000
    targetPort: 5000
  selector:
    app: registry
```

Apply these configurations:

```
bash

kubectl apply -f registry-deployment.yaml
kubectl apply -f registry-service.yaml
```

Update Image Tagging

If your registry is running inside the Kubernetes cluster, you'll need to tag the images accordingly:

```
bash

docker tag yourusername/kafka-producer:latest <cluster-ip>:5000/kafka-producer:latest
```

Push the image:
```
bash

docker push <cluster-ip>:5000/kafka-producer:latest
```
### Configure Kubernetes to Use the Private Registry

If your Kubernetes cluster nodes do not have access to the private registry by default, you need to configure them to trust your registry. This involves setting up an image pull secret if your registry requires authentication.
Create a Secret for Registry Authentication (if needed)

```
bash

kubectl create secret docker-registry regcred \
  --docker-server=<registry-server> \
  --docker-username=<your-username> \
  --docker-password=<your-password> \
  --docker-email=<your-email> \
  --namespace=kafka-pipeline
```

Update your deployment to use the image pull secret:
```
yaml

# kafka-producer-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-producer
  namespace: kafka-pipeline
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka-producer
  template:
    metadata:
      labels:
        app: kafka-producer
    spec:
      imagePullSecrets:
      - name: regcred
      containers:
      - name: kafka-producer
        image: <registry-server>/kafka-producer:latest
        env:
        - name: KAFKA_BROKER
          value: "kafka:9092"
```

### Replace .env credentials by kubernetes credentials
.env files is not used by kubernetes, instead ```Base64``` encoded properties should be added. 

To make them secure we have to generate encryption-config which is also should be passed to our server which runs kubernetes cluster. 

In case of ```minikube``` it looks like:
```
minikube ssh "sudo mkdir -p /etc/kubernetes/"
scp -i $(minikube ssh-key) encryption-config.yaml docker@$(minikube ip):/home/docker/
minikube ssh "sudo mv /home/docker/encryption-config.yaml /etc/kubernetes/encryption-config.yaml"
```

Add this path to a custom encryption config to yaml file --encryption-provider-config=/etc/kubernetes/
```
sudo vi /etc/kubernetes/manifests/kube-apiserver.yaml

spec:
  containers:
  - command:
    - kube-apiserver
      - ... /* others configs */
      - --encryption-provider-config=/etc/kubernetes/encryption-config.yaml
```

### Apply the Kubernetes Manifests
```
bash

kubectl apply -f namespace.yaml
kubectl apply -f zookeeper-deployment.yaml
kubectl apply -f zookeeper-service.yaml
kubectl apply -f kafka-deployment.yaml
kubectl apply -f kafka-service.yaml
kubectl apply -f connect-deployment.yaml
kubectl apply -f connect-service.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f rest-server-deployment.yaml
kubectl apply -f rest-server-service.yaml
kubectl apply -f kafka-producer-deployment.yaml
kubectl apply -f postgres-secret.yaml
kubectl apply -f registry-deployment.yaml (optional)
kubectl apply -f registry-service.yaml (optional)
```