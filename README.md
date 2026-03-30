# LogInsight

## Overview
LogInsight is a cloud-native log processing pipeline designed to detect error patterns and anomalies from operational logs.

The system follows a scalable, production-style architecture with decoupled ingestion, containerized deployment, and cloud storage integration.

---

## Project Goals

This project is designed to demonstrate:

- Cloud-native system design
- Distributed log processing architecture
- Scalable and resilient services
- CI/CD and DevOps practices

---

## Features
- Log pattern extraction & error aggregation
- Anomaly detection (lightweight statistical approach)
- Scalable multi-instance deployment with Nginx load balancing
- Cloud storage integration (AWS S3)
- Containerized with Docker
- Automated CI/CD pipeline (GitHub Actions → Docker Hub → EC2)

---

## Architecture

### Current (Deployed)

Client → Nginx (Load Balancer) → FastAPI (Multi-instance)
                                  ↓
                                Analyzer
                                  ↓
                                 S3

---

### Target Cloud Architecture (In Progress)

Client
  ↓
API Gateway
  ↓
Ingestion Layer (Lambda / API)
  ↓
Queue (SQS)
  ↓
Worker (Auto Scaling)
  ↓
S3 (Raw / Processed Logs)
  ↓
Monitoring (CloudWatch)

---

## Key Concepts

- **Load Balancing**: Nginx distributes traffic across multiple FastAPI instances
- **Scalability**: Services can be horizontally scaled via Docker Compose or cloud auto scaling
- **Decoupling (planned)**: Queue-based ingestion using SQS
- **Durable Storage**: Logs stored in AWS S3
- **Cloud-ready**: Designed for migration to AWS managed services

---

## CI/CD

Pipeline:

Push to main  
→ GitHub Actions  
→ Build Docker Image  
→ Push to Docker Hub  
→ Deploy to EC2  
→ Restart services with scaling  

---

## API Usage

### Health Check

```bash
curl http://<EC2-IP>/health
```

### Ingest Logs

```bash
curl -X POST http://<EC2-IP>/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "logs": [
      {"timestamp": "2026-03-30T10:00:00", "level": "ERROR", "message": "DB timeout", "service": "auth"}
    ]
  }'
```

### Analyze Logs

```bash
curl http://<EC2-IP>/analyze
```

Return: 

```bash
{
  "error_count": 2,
  "top_errors": [
    "Failed to connect to DB",
    "DB timeout"
  ],
  "anomaly_score": 0.67
}
```

### Reset Logs

```bash
curl -X POST http://<EC2-IP>/reset
```
---

## Multi-instance Deployment (with Nginx)

Start services with scaling:

```bash
docker-compose up -d --scale log-insight=3
```

---

## AWS S3 Integration

Environment variables:

```bash
AWS_REGION=<your-region>
S3_BUCKET=<your-bucket>
```

Logs are automatically uploaded to S3 for persistent storage.

---

## Summary

LogInsight evolves from a simple log analysis API into a cloud-ready observability pipeline, focusing on scalability, decoupling, and production-grade architecture.

---