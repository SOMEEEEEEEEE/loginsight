#Cloud-Native LogInsight – k3s Deployment

This branch is a cloud-native log ingestion system designed to run on Kubernetes (k8s).
It demonstrates containerised services and basic DevOps practices. 

---

## Structure
```
.
├── services/
│   └── ingest/              # Log ingestion service
├── shared/                  # Common utilities
├── deploy/
│   └── k8s/                 # Kubernetes manifests
│       ├── ingest-deployment.yaml
│       └── ingest-service.yaml
├── docker/
├── docker-compose.yml
└── README.md

```

## Sample
### 1. Build Image
```
docker build -t loginsight-ingest ./services/ingest
```

### 2. Import into k8s
```
sudo docker save loginsight-ingest | sudo k8s ctr images import -
```

### 3. Deploy
```
kubectl apply -f deploy/k8s/
```
Check: 
```
kubectl get pods
kubectl get svc
```

### 4. Access
```
kubectl port-forward svc/ingest 8000:8000
```

---

## Dev Loop
```
docker build -t loginsight-ingest .
sudo docker save loginsight-ingest | sudo k3s ctr images import -
kubectl rollout restart deployment ingest
```

---

## Next
- Probes (liveness/readiness)
- ConfigMap
- Helm
- CI/CD

