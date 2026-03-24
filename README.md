# Taxi Duration Prediction Service

A lightweight **Flask-based web service** for predicting NYC taxi trip duration from trip features such as pickup location, dropoff location, and trip distance.

This project can be run in two ways:

1. **Directly as a local web service**
2. **Inside a Docker container**

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Input Features](#input-features)
- [Requirements](#requirements)
- [Run Locally as a Web Service](#run-locally-as-a-web-service)
- [API Usage](#api-usage)
  - [POST Request](#post-request)
  - [GET Request](#get-request)
- [Run with Docker](#run-with-docker)
- [Testing the Service](#testing-the-service)
- [Common Issues](#common-issues)
- [Future Improvements](#future-improvements)

---

## Overview

This service loads a trained machine learning model from disk and exposes a prediction API through Flask.

Given:

- `PULocationID`
- `DOLocationID`
- `trip_distance`

the service prepares the input features, transforms them with a saved `DictVectorizer`, and returns the predicted trip duration.

The current application listens on:

- **Host:** `0.0.0.0`
- **Port:** `9696`

---

## Project Structure

```text
taxi-duration-prediction-service/
│
├── predict.py                  # Flask application
├── models/
│   └── linear_model.joblib     # Saved DictVectorizer + trained model
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition (if present)
└── README.md                   # Project documentation
```

---

## How It Works

The main service logic is implemented in `predict.py`.

### Core flow

1. Load the saved model artifact from:

   ```text
   ./models/linear_model.joblib
   ```

2. Build features from the incoming ride payload:

   - `DO_PU = "{DOLocationID}_{PULocationID}"`
   - `trip_distance`

3. Transform features using the saved `DictVectorizer`
4. Run prediction with the trained model
5. Return the prediction as JSON

---

## Input Features

The API expects the following fields:

| Field | Type | Description |
|------|------|-------------|
| `PULocationID` | `int` | Pickup location ID |
| `DOLocationID` | `int` | Dropoff location ID |
| `trip_distance` | `float` | Distance of the trip |

### Example input

```json
{
  "PULocationID": 130,
  "DOLocationID": 205,
  "trip_distance": 3.66
}
```

---

## Requirements

- Python 3.9+ recommended
- `pip`
- Docker Desktop installed if running in a container

Typical Python dependencies:

- `flask`
- `joblib`
- `scikit-learn`

If `requirements.txt` exists, install dependencies from it.

---

## Run Locally as a Web Service

### 1. Open the project directory

On macOS:

```bash
cd <project_directory>
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Make sure the trained model exists

The service expects this file:

```text
./models/linear_model.joblib
```

If it is missing, place the trained model artifact there before starting the service.

### 5. Start the Flask app

```bash
python predict.py
```

or with gunicorn

```bash
gunicorn -b 0.0.0.0:9696 predict:app
```

If successful, app starts on:

```text
http://0.0.0.0:9696
```

From the local machine, access it using:

```text
http://localhost:9696
```
---

## API Usage

The service exposes the same route `/predict` for both:

- `POST`
- `GET`

---

### POST Request

Use a JSON body.

#### Example with `curl`

```bash
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{
    "PULocationID": 130,
    "DOLocationID": 205,
    "trip_distance": 3.66
  }'
```

#### Example response

```json
15.90
```

---

### GET Request

Pass values as query parameters.

#### Example with `curl`

```bash
curl "http://localhost:9696/predict?PULocationID=130&DOLocationID=205&trip_distance=3.66"
```

#### Example response

```json
15.90
```

---

## Run with Docker

If a `Dockerfile` is already present in the project, use the following steps.

### 1. Build the Docker image

From the project root:

```bash
docker build -t taxi-duration-prediction-service .
```

### 2. Run the container

```bash
docker run -it --rm -p 9696:9696 taxi-duration-prediction-service
```

This maps:

- container port `9696`
- to local port `9696`

The service will then be available at:

```text
http://localhost:9696
```

### 3. Test the running container

#### POST request

```bash
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{
    "PULocationID": 130,
    "DOLocationID": 205,
    "trip_distance": 3.66
  }'
```

#### GET request

```bash
curl "http://localhost:9696/predict?PULocationID=130&DOLocationID=205&trip_distance=3.66"
```

---

## Testing the Service

After starting the application locally or in Docker, verify that:

- Flask starts without import errors
- `./models/linear_model.joblib` is found
- requests to `/predict` return numeric JSON output

A valid response should be a predicted duration value.

---

## Common Issues

### 1. `FileNotFoundError: ./models/linear_model.joblib`

**Cause:** The trained model file is missing.

**Fix:** Ensure the file exists at:

```text
models/linear_model.joblib
```

---

### 2. `ModuleNotFoundError`

**Cause:** Required Python packages are not installed.

**Fix:**

```bash
pip install -r requirements.txt
```

---

### 3. Docker builds but container fails at runtime

**Cause:** Model file may not be copied into the image.

**Fix:** Ensure the `models/` directory and `linear_model.joblib` are included in the Docker image.

---

### 4. Port already in use

**Cause:** Another process is already using port `9696`.

**Fix:** Stop the other process or use a different port mapping:

```bash
docker run -it --rm -p 9697:9696 taxi-duration-prediction-service
```

Then call:

```text
http://localhost:9697
```

---

## Future Improvements

Possible enhancements for this project:

- Add request validation
- Return structured JSON like:

  ```json
  {
    "predicted_duration": 15.90
  }
  ```

- Load the model once at app startup instead of on every request
- Add health check endpoint such as `/health`
- Add logging
- Add unit and integration tests
- Support multiple model versions

---

## Example End-to-End Workflow

### Local

```bash
cd <project_directory>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python predict.py
```

In a second terminal:

```bash
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{"PULocationID":130,"DOLocationID":205,"trip_distance":3.66}'
```

### Docker

```bash
cd <project_directory>
docker build -t taxi-duration-prediction-service .
docker run -it --rm -p 9696:9696 taxi-duration-prediction-service
```

In a second terminal:

```bash
curl "http://localhost:9696/predict?PULocationID=130&DOLocationID=205&trip_distance=3.66"
```

---

## License

Add your preferred license here, for example MIT.

---

## Author

Personal ML learning project focused on model serving and containerized deployment.