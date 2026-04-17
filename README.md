# LogInsight (Cloud-Native Async Log Analysis)

A minimal cloud‑native log processing pipeline built with **FastAPI + AWS SQS + AWS S3 + Worker**.
The system ingests logs, processes them asynchronously, stores results in S3, and provides query APIs.

---

## Architecture

```
Client
   ↓
Ingest API (FastAPI)
   ↓
AWS SQS  → Worker (Async Processor)
                  ↓
               AWS S3
                  ↓
            Query API (FastAPI)
```

---

## Project Structure

```
loginsight/
│
├─ ingest/                  # ingestion service
│   ├─ main.py
│   ├─ routes/logs.py
│   └─ services/log_service.py
│
├─ query/                   # query service
│   ├─ main.py
│   ├─ routes/results.py
│   └─ services/result_service.py
│
├─ worker/                  # async worker
│   ├─ main.py
│   └─ processor.py
│
├─ common/                  # shared modules
│   ├─ sqs_client.py
│   ├─ s3_client.py
│   ├─ s3_service.py
│   ├─ analyzer.py
│   ├─ models.py
│   └─ utils.py
│
├─ nginx/
│   └─ nginx.conf
│
├─ docker-compose.yml
└─ .env
```

---

## Features

* Async log ingestion using AWS SQS
* Batch log processing worker
* Structured log analysis
* Result storage in AWS S3
* Query results by task_id
* Cloud‑native microservice design
* Horizontal worker scalability

---

## Environment Variables

In `.env` file:

```
AWS_REGION=eu-west-1
SQS_QUEUE_URL=YOUR_SQS_URL
S3_BUCKET=YOUR_BUCKET
```

---

## Run on EC2 (venv)

### 1. Create virtual environment and install dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn boto3 pydantic
```

---

### 2. Start Services (Background)

#### 2.1 Start ingest service

```
nohup venv/bin/uvicorn ingest.main:app \
  --host 0.0.0.0 \
  --port 8001 \
  > ingest.log 2>&1 &
```

#### 2.2 Start query service

```
nohup venv/bin/uvicorn query.main:app \
  --host 0.0.0.0 \
  --port 8002 \
  > query.log 2>&1 &
```

#### 2.3 Start worker

```
nohup venv/bin/python worker/main.py > worker.log 2>&1 &
```

---

### 3. Check Running Services

```
ps aux | grep uvicorn
ps aux | grep worker/main
```

---

### 4. View Logs

```
tail -f ingest.log
tail -f worker.log
tail -f query.log
```

---

### 5. Stop Services

```
pkill -f "uvicorn ingest"
pkill -f "uvicorn query"
pkill -f "worker/main.py"
```

---

## API Usage

### Ingest Logs

POST /logs

```
curl -X POST http://localhost:8001/logs \
-H "Content-Type: application/json" \
-d '{
  "logs": [
    {"message": "error occurred", "level": "ERROR"},
    {"message": "service started", "level": "INFO"}
  ]
}'
```

Response:

```
{
  "status": "queued",
  "task_id": "uuid",
  "message_id": "sqs-id",
  "count": 2
}
```

---

### Query Result

```
GET /results/{task_id}
```

Example:

```
curl http://localhost:8002/results/<task_id>
```

Processing:

```
{
  "task_id": "...",
  "status": "processing"
}
```

Completed:

```
{
  "task_id": "...",
  "status": "completed",
  "result": {...}
}
```

---

## S3 Storage Format

Results stored as:

```
results/{task_id}.json
```

Example:

```
results/123e4567-e89b.json
```

---

## Scaling

Worker can scale horizontally:

```
python worker/main.py
python worker/main.py
python worker/main.py
```

All workers consume from same SQS queue.

---

## Future Improvements

* Add Redis cache for result lookup
* Add CloudWatch metrics
* Add batching optimization
* Add retry dead-letter queue
* Add dashboard UI
* Add Terraform deployment

---

## Platform Evolution Roadmap
This project is evolving from a minimal async log pipeline into a cloud-native DevOps platform.

### Phase 1 — Containerized Microservices (Completed)
* Split ingest / query / worker services
* Introduce shared common module
* Async processing via SQS
* S3-based result storage
* Nginx reverse proxy
Phase 2 — Cloud-Native Deployment (In Progress)
* Docker Compose multi-service deployment
* Environment-based configuration (.env)
* Service health checks
* Production-ready container images
Phase 3 — Kubernetes Platform
* Kubernetes deployment manifests
* Service & ingress configuration
* Horizontal worker scaling
* ConfigMap & Secrets support
Phase 4 — Infrastructure as Code
* Terraform infrastructure definition
* Cloud resource provisioning
* Environment separation (dev/staging/prod)
* Automated deployment workflows
Phase 5 — CI/CD & DevOps Enablement
* GitHub Actions CI pipeline
* Container image build & publish
* Kubernetes deployment automation
* Release versioning
Phase 6 — Observability & Reliability
* Structured logging
* Metrics collection
* Health checks & readiness probes
* Failure retry & DLQ support

---

## Tech Stack

* FastAPI
* AWS SQS
* AWS S3
* Python
* Docker (optional)
* Nginx (optional)

---

## End-to-End Flow

```
POST /logs
     ↓
   SQS
     ↓
 Worker
     ↓
   S3
     ↓
GET /results/{task_id}
```

