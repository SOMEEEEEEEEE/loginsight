# Log Insight Platform

## Overview

Log Insight Platform is a cloud-native incident processing system designed to demonstrate asynchronous event-driven architecture using Python and AWS-style messaging patterns.

The system accepts incident requests through an API layer, places them onto a message queue, and processes them asynchronously through background workers.

The project focuses on:

- Python application development
- Asynchronous processing
- Message queue integration
- Structured logging
- Containerized deployment
- Cloud-native architecture patterns

---

## High-Level Architecture

Client
│
▼
API Service (FastAPI)
│
▼
SQS Queue
│
▼
Worker Service
│
▼
Incident Processor
│
▼
Structured Logs

---

## Components

### API Service

Responsibilities:

- Receive incident requests
- Validate input data
- Publish messages to queue
- Return immediate response

Benefits:

- Fast response times
- Decoupled from processing logic
- Easier horizontal scaling

---

### Queue Layer

Responsibilities:

- Buffer incoming requests
- Decouple API and worker services
- Improve resilience during traffic spikes

Current implementation:

- AWS SQS

Benefits:

- Reliable message delivery
- Independent scaling
- Reduced service coupling

---

### Worker Service

Responsibilities:

- Poll messages from queue
- Process incidents
- Generate operational logs
- Handle processing failures

Benefits:

- Background processing
- Independent deployment
- Scalable worker pool model

---

### Incident Processor

Responsibilities:

- Execute incident handling logic
- Transform input data
- Generate processing results

Benefits:

- Clear separation of business logic
- Easier testing
- Improved maintainability

---

### Logging

Current logging strategy:

- Structured JSON logging
- Service identification
- Context-aware log fields

Example:

{
  "service": "worker",
  "message": "processing incident",
  "incident_id": "123"
}

Benefits:

- Easier troubleshooting
- Better observability
- Machine-readable logs

---

## Project Structure

log-insight-platform
├── api/
├── worker/
├── shared/
├── platform/
├── docs/
├── tests/
└── docker/

---

## Current Workflow

1. Client submits incident request
2. API validates request
3. API publishes message to SQS
4. Worker retrieves message
5. Processor handles incident
6. Structured logs are generated
7. Message is removed from queue

---

## Design Decisions

### Why Queue-Based Processing?

To separate request handling from background processing.

Benefits:

- Improved responsiveness
- Better scalability
- Failure isolation

### Why Separate API and Worker?

To follow single-responsibility principles.

API:

- Accept requests

Worker:

- Process requests

Benefits:

- Independent scaling
- Cleaner architecture
- Easier maintenance

### Why Structured Logging?

To support operational monitoring and troubleshooting.

Benefits:

- Consistent log format
- Easier filtering and analysis
- Better support for centralized logging systems

---

## Future Improvements

Potential next steps:

- Terraform infrastructure provisioning
- AWS ECS deployment
- CI/CD pipeline
- Metrics and monitoring
- Retry and dead-letter queue support
- Automated testing expansion
