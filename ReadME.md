# Claim Management System

## Overview
Claim Management System is a FastAPI application that allows users to to process and manage healthcare
claims and generate CSV reports of claims grouped by status. The application uses Celery with Redis to handle report generation in the background.

## Features
- User authentication with JWT.
- Create, read, update, and delete claims.
- Generate CSV reports of claims grouped by status.
- Asynchronous report generation using Celery and Redis.
- Download generated reports via a simple API.

## Technologies
- **Backend**: FastAPI
- **Task Queue**: Celery
- **Message Broker**: Redis
- **Database**: SQLite (or any other database as needed)
- **Data Handling**: Pandas for CSV generation

## Getting Started

### Prerequisites
- Python 3.8 and above
- Redis server installed and running
- Required Python packages (see `requirements.txt`)
- Run 'db.py' file to create the DB

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kareemAL-Harkeh/Claim-Management-System.git
   cd claim-report-generator