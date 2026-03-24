# LogInsight

## Overview
A production-style log analysis service that detects error patterns and anomalies from operational logs, with automated CI/CD and cloud deployment.

## Features
- Log pattern extraction
- Error aggregation
- Anomaly detection

## Architecture

 	Client → API → Analyzer → Result
 		↓
 		Docker
 		↓
 		Docker Hub
 		↓
 		*EC2 (pull image)


## *CI/CD
- Push to main → GitHub Actions → Build Docker → Push to Docker Hub → *Deploy to EC2 (Pull Image)

## *Example
curl -X POST http://<EC2-IP>/analyze \
-H "Content-Type: application/json" \
-d '{"logs":["ERROR db timeout","INFO ok"]}'