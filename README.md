# ML Production API

A production-style REST API that serves a trained machine learning model for **next-day Delhi PM2.5 prediction**.

This project takes the XGBoost PM2.5 model developed in the earlier air-quality prediction project and converts it into a reusable API using **FastAPI**, with input validation, automated tests, interactive API documentation, and Docker containerization.

## Project Overview

Machine learning models are useful only when they can be integrated into applications and services.

This project focuses on the deployment side of machine learning by taking an already-trained PM2.5 prediction model and exposing it through a REST API.

The API accepts historical PM2.5 and temporal features as JSON and returns a predicted next-day PM2.5 concentration.

The complete system is:

```text
Trained XGBoost Model
        ↓
FastAPI REST API
        ↓
Pydantic Input Validation
        ↓
Prediction Endpoint
        ↓
Docker Container
        ↓
Deployable ML Service
```

---

## Objectives

The main objectives of this project are:

* Serve a trained machine learning model through an API
* Build REST endpoints using FastAPI
* Validate incoming prediction data
* Load a serialized machine learning model
* Return structured JSON predictions
* Create automated API tests
* Containerize the application using Docker
* Provide interactive API documentation through Swagger UI
* Structure an ML project for production-style deployment

---

## Model

The API uses the **XGBoost PM2.5 regression model** developed for the Delhi PM2.5 prediction project.

The model is stored as:

```text
model/xgboost_pm25_model.pkl
```

The model expects the following 10 features:

```text
lag_1
lag_2
lag_3
lag_7
rolling_3
rolling_7
rolling_14
day_of_week
day_of_year
week_of_year
```

The model predicts:

```text
Next-day PM2.5 concentration
```

Unit:

```text
µg/m³
```

---

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn

### Machine Learning

* XGBoost
* Scikit-learn
* Joblib
* Pandas

### API Validation

* Pydantic

### Testing

* Pytest
* FastAPI TestClient
* HTTPX

### Containerization

* Docker

### Version Control

* Git
* GitHub

---

## Project Structure

```text
project-06-ml-production-api/
│
├── app/
│   └── main.py
│
├── model/
│   └── xgboost_pm25_model.pkl
│
├── schemas/
│
├── tests/
│   └── test_api.py
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

---

# API Architecture

The API follows a simple request-response architecture:

```text
Client
  │
  │ JSON Request
  ↓
FastAPI
  │
  ↓
Pydantic Validation
  │
  ↓
Feature DataFrame
  │
  ↓
XGBoost Model
  │
  ↓
Prediction
  │
  ↓
JSON Response
```

---

# API Endpoints

## GET `/`

Basic API information and availability check.

### Response

```json
{
  "message": "Delhi PM2.5 Prediction API is running"
}
```

---

## GET `/health`

Health-check endpoint used to verify that the API is running correctly.

### Response

```json
{
  "status": "healthy"
}
```

---

## POST `/predict`

Generates a next-day PM2.5 prediction from the supplied historical and temporal features.

### Request

```json
{
  "lag_1": 85.4,
  "lag_2": 91.2,
  "lag_3": 78.6,
  "lag_7": 102.3,
  "rolling_3": 85.1,
  "rolling_7": 88.4,
  "rolling_14": 92.7,
  "day_of_week": 2,
  "day_of_year": 265,
  "week_of_year": 39
}
```

### Response

```json
{
  "predicted_pm25": 87.42,
  "unit": "µg/m³"
}
```

The exact prediction depends on the trained model and supplied feature values.

---

# Input Validation

The API uses Pydantic to validate incoming requests before they reach the machine learning model.

### PM2.5 Features

PM2.5-related features must be non-negative:

```text
lag_1 >= 0
lag_2 >= 0
lag_3 >= 0
lag_7 >= 0

rolling_3 >= 0
rolling_7 >= 0
rolling_14 >= 0
```

### Calendar Features

The temporal features are constrained to valid ranges:

```text
day_of_week: 0–6
day_of_year: 1–366
week_of_year: 1–53
```

Invalid requests are automatically rejected by FastAPI with a validation error instead of being passed to the model.

---

# Interactive API Documentation

FastAPI automatically generates interactive API documentation.

After starting the application, open:

```text
http://127.0.0.1:8000/docs
```

The Swagger UI allows users to:

* View available endpoints
* Inspect request schemas
* Enter prediction inputs
* Execute API requests
* View JSON responses
* Test the API without an external API client

---

# Running Locally

Clone the repository:

```bash
git clone https://github.com/ayushi-stacks/ML-production-API.git
```

Move into the project:

```bash
cd project-06-ml-production-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Testing

Automated tests are implemented using Pytest and FastAPI's `TestClient`.

The test suite checks:

* Root endpoint
* Health endpoint
* Prediction endpoint
* Prediction response structure
* Returned prediction type
* Returned measurement unit

Run the tests using:

```bash
pytest
```

Expected result:

```text
3 passed
```

---

# Docker

The API is containerized using Docker.

## Build the Image

From the project root:

```bash
docker build -t pm25-api .
```

## Run the Container

```bash
docker run --rm -p 8000:8000 pm25-api
```

The API will then be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# Docker Architecture

```text
Docker Container
│
├── Python 3.12
│
├── FastAPI
│
├── Uvicorn
│
├── XGBoost
│
├── Scikit-learn
│
├── Pandas
│
├── Joblib
│
└── Trained PM2.5 Model
```

The Docker image contains everything required to run the API independently of the local Python environment.

---

# Dockerfile

The application uses a lightweight Python image:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY model ./model

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# Example Request

A client can send a POST request to `/predict` containing:

```json
{
  "lag_1": 85.4,
  "lag_2": 91.2,
  "lag_3": 78.6,
  "lag_7": 102.3,
  "rolling_3": 85.1,
  "rolling_7": 88.4,
  "rolling_14": 92.7,
  "day_of_week": 2,
  "day_of_year": 265,
  "week_of_year": 39
}
```

The API processes the request through the trained model and returns the predicted PM2.5 concentration.

---

# Development Workflow

The project follows this workflow:

```text
Existing ML Model
       ↓
Model Serialization
       ↓
FastAPI Integration
       ↓
Request Schema
       ↓
Input Validation
       ↓
Prediction Endpoint
       ↓
Automated Testing
       ↓
Dockerization
       ↓
Containerized API
```

---

# Production-Oriented Features

Although this is a portfolio project, it incorporates several practices used in production ML services:

* REST API architecture
* Explicit request schemas
* Input validation
* Health-check endpoint
* Serialized model loading
* Automated testing
* Containerization
* Interactive API documentation
* Separation of model and application code
* Reproducible dependency installation

---

# Limitations

The current API has several limitations:

* The model is based on a single PM2.5 monitoring location.
* Predictions depend on the quality and distribution of the original training data.
* The API does not automatically retrieve the latest OpenAQ measurements.
* Users currently provide the model features manually.
* There is no authentication layer.
* There is no rate limiting.
* There is no production monitoring system.
* There is no automated model retraining pipeline.
* Prediction uncertainty is not currently returned.

---

# Future Improvements

Potential improvements include:

* Connect the API directly to OpenAQ
* Automatically calculate prediction features
* Add authentication
* Add API rate limiting
* Add structured logging
* Add monitoring and observability
* Add prediction confidence or uncertainty estimates
* Add automated model retraining
* Add CI/CD using GitHub Actions
* Deploy the Docker container to a cloud platform
* Add API versioning
* Add request and prediction logging
* Add model performance monitoring
* Add integration tests
* Add Redis or another caching layer
* Add database-backed prediction history

---

# Skills Demonstrated

This project demonstrates practical experience with:

### Machine Learning Engineering

* Model serialization
* Model serving
* Feature schema design
* Prediction pipelines

### Backend Development

* REST APIs
* FastAPI
* HTTP endpoints
* JSON request/response handling
* API validation

### Software Engineering

* Project structure
* Automated testing
* Dependency management
* Error prevention through validation

### DevOps

* Docker
* Containerized application deployment
* Reproducible environments

### Developer Tools

* Git
* GitHub
* Swagger/OpenAPI
* Pytest

---

# Project Outcome

The project converts a trained machine learning model into a reusable service:

```text
Machine Learning Model
        ↓
FastAPI
        ↓
Validated REST Endpoint
        ↓
Automated Tests
        ↓
Docker Container
        ↓
Deployable ML API
```

Instead of running the model directly from a notebook or Python script, other applications can now communicate with it through a standard HTTP API.

---

# Author

**Ayushi Mandal**

B.Tech Information Technology
University of Calcutta

Interested in Machine Learning, Artificial Intelligence, Software Development, UI/UX Design, and building practical technology projects.

---

## Related Project

This API uses the model developed in the Delhi PM2.5 Prediction project.

**Previous project:** Delhi PM2.5 Prediction

The earlier project covers:

* OpenAQ data collection
* Exploratory Data Analysis
* Feature engineering
* Model comparison
* XGBoost regression
* Streamlit deployment

This project extends that work into a production-style ML API.
