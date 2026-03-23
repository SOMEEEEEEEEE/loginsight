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
	*EC2

## *CI/CD
- Push to main → GitHub Actions → Build Docker → Deploy to EC2

## *Example
curl -X POST http://<EC2-IP>/analyze \
-H "Content-Type: application/json" \
-d '{"logs":["ERROR db timeout","INFO ok"]}'