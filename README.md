# LogInsight

## Overview
A production-style log analysis service that detects error patterns and anomalies from operational logs, with automated CI/CD and cloud deployment.

## Features
- Log pattern extraction
- Error aggregation & Anomaly detection
- Cloud-ready: easily deployable on AWS EC2 or other cloud VMs
- Dockerized for scalable deployments

## Architecture

 	Client → API → Analyzer → Result
 		↓
 		Docker
 		↓
 		Docker Hub
 		↓
 		EC2 (pull image)


## CI/CD
- Push to main → GitHub Actions → Build Docker → Push to Docker Hub → Deploy to EC2

## Example

### Health check: 

```bash
curl http://localhost/
```

or 

```bash
curl http://<EC2-IP>/
```

### Send logs for analysis:

```bash
curl -X POST http://localhost:80/ingest \
     -H "Content-Type: application/json" \
     -d '{"log": "ERROR Something went wrong"}'
```

Return: 

```bash
{"msg":"3 logs ingested","total_logs":3}
```

### Get the results: 

```bash
curl http://localhost:80/analyze
```

Return: 

```bash
{
	"error_count":2,
	"top_errors":[
		"Failed to connect to DB",
		"DB timeout"
	],
	"anomaly_score":0.67
}
```

### Reset stored logs: 

```bash
curl -X POST http://localhost:80/reset
```

## Run locally: 

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker

```bash
docker build -t log-insight .
docker run -d -p 8000:8000 log-insight
```
