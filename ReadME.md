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
- Run `db.py` file to create the DB

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kareemAL-Harkeh/Claim-Management-System.git



## Examples of API Usage

Here are some examples of how to use the API endpoints with cURL commands.

### User Authentication

#### Signup
To create a new user, you can use the following cURL command:

```bash
curl -X "POST" \
  'http://localhost:8000/auth/signup/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "name",
  "password": "pass"
}'
```

#### Login
To Login, you can use the following cURL command:
```bash
curl -X 'POST' \
  'http://localhost:8000/auth/login/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=name&password=pass&scope=&client_id=string&client_secret=string'
```

### Claims Management

#### Create a Claim
To Create a Claim, you can use the following cURL command:

```bash
curl -X 'POST' \
  'http://localhost:8000/claims/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYXJlZW0iLCJleHAiOjE3MzczMjUyNDl9.9GnncFp8xYW1KRHMUu_Nnn0ayehB5PD9vyhfH0yIyRY' \
  -H 'Content-Type: application/json' \
  -d '{
  "patient_name": "string6",
  "diagnosis_code": "string6",
  "procedure_code": "string6",
  "claim_amount": 6
}'
```

#### Get All Claims
To Get All Claims, you can use the following cURL command:

```bash
curl -X 'GET' \
  'http://localhost:8000/claims/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYXJlZW0iLCJleHAiOjE3MzczMjYwNzJ9.ID0Dm11kRbTBgAlTosmJOzHve6Tp8ciTXnLjeUwTYTw'
```

#### Get Cliams Filtered By Status
To Get Cliams Filtered By Status, you can use the following cURL command:

```bash
curl -X 'GET' \
  'http://localhost:8000/claims/?status=APPROVED' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYXJlZW0iLCJleHAiOjE3MzczMjUyNDl9.9GnncFp8xYW1KRHMUu_Nnn0ayehB5PD9vyhfH0yIyRY'
```

#### Get Cliams Filtered By diagnosis_code
To Get Cliams Filtered By diagnosis_code, you can use the following cURL command:

```bash
curl -X 'GET' \
  'http://localhost:8000/claims/?diagnosis_code=string2' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYXJlZW0iLCJleHAiOjE3MzczMjYwNzJ9.ID0Dm11kRbTBgAlTosmJOzHve6Tp8ciTXnLjeUwTYTw'
```

#### Get Cliams Filtered By procedure_code
To Get Cliams Filtered By procedure_code, you can use the following cURL command:

```bash
curl -X 'GET' \
  'http://localhost:8000/claims/?procedure_code=string2' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYXJlZW0iLCJleHAiOjE3MzczMjYwNzJ9.ID0Dm11kRbTBgAlTosmJOzHve6Tp8ciTXnLjeUwTYTw'
```

####  Get Claim Detail
To Get Claim By ID, you can use the following cURL command:

```bash
curl -X 'GET' \
  'http://localhost:8000/claims/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYXJlZW0iLCJleHAiOjE3MzczMjYwNzJ9.ID0Dm11kRbTBgAlTosmJOzHve6Tp8ciTXnLjeUwTYTw'
```

#### Update Claim's Status
To Update a Claim's status, you can use the following cURL command:

```bash
curl -X 'PUT' \
  'http://localhost:8000/claims/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYXJlZW0iLCJleHAiOjE3MzczMjYwNzJ9.ID0Dm11kRbTBgAlTosmJOzHve6Tp8ciTXnLjeUwTYTw' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "DENIED"
}'
```

#### Delete Claim
To Delete a claim by its ID, you can use the following cURL command:

```bash
curl -X 'DELETE' \
  'http://localhost:8000/claims/6' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYXJlZW0iLCJleHAiOjE3MzczMjYwNzJ9.ID0Dm11kRbTBgAlTosmJOzHve6Tp8ciTXnLjeUwTYTw'
```

#### Generate a CSV Report 
To generate a CSV report of all claims, grouped by status with total claim amounts.

```bash
curl -X 'POST' \
  'http://localhost:8000/claims/report' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYXJlZW0iLCJleHAiOjE3MzczMjYwNzJ9.ID0Dm11kRbTBgAlTosmJOzHve6Tp8ciTXnLjeUwTYTw' \
  -d ''
```

#### Check Report
Check the status of the report generation and provide a link to download it once ready

```bash
curl -X 'GET' \
  'http://localhost:8000/claims/report/e9632230-b4df-49b6-bb43-8bbda9da23e8' \
  -H 'accept: application/json'
```