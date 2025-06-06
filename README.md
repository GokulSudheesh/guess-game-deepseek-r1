# Guess Game App

A silly guess game for testing out the thinking capability of deep seek model hosted on NVIDIA builder.

## Project Structure

- `guess-game-be/` — Backend API built with Python (FastAPI).

## Getting Started

#### Setting up NVIDIA Builder

- Go to <https://build.nvidia.com/deepseek-ai/deepseek-r1>, create an account and get the API Key.
- Create an `.env` file under `guess-game-be/` with the following content:

  ```dotenv
  ENVIRONMENT=local
  NVIDIA_API_KEY=your_api_key_here
  NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
  NVIDIA_MODEL_NAME=deepseek-ai/deepseek-r1
  PLATFORM_TO_USE=nvidia
  ```

#### Alternative Setup for OLLAMA

- If you prefer to run it locally and wanna use OLLAMA instead of NVIDIA Builder, download <https://ollama.com>.
- Run the following command to pull and run the model:

  ```bash
  ollama run deepseek-r1
  ```

- Create an `.env` file under `guess-game-be/` with the following content:

  ```dotenv
  ENVIRONMENT=local
  OLLAMA_BASE_URL=your_local_ollama_url_here
  OLLAMA_MODEL_NAME=deepseek-r1
  PLATFORM_TO_USE=ollama
  ```

### Settung up FastAPI

- Install the required packages with poetry:

  ```bash
  poetry install
  poetry run uvicorn app.main:app
  ```

## API Endpoints

##### `POST /api/v1/guess/start` — Initiate a session

**Curl**

```bash
curl --location --request POST 'http://localhost:8000/api/v1/guess/start'
```

**Sample Response**

```json
{
  "success": true,
  "data": {
    "session_id": "f3e9c2bb-349b-4da2-8dac-c15bdfea889c",
    "question": "Is the person you're thinking of a fictional character?",
    "guess": null,
    "confidence": 0.0,
    "question_number": 1
  }
}
```

##### `POST /api/v1/guess/ask` — Answer to the bot's yes / no question

**Curl**

```bash
curl --location 'http://localhost:8000/api/v1/guess/ask' \
--header 'Content-Type: application/json' \
--data '{
    "session_id": "f3e9c2bb-349b-4da2-8dac-c15bdfea889c",
    "answer": "YES"
}'
```

**Sample Response**

```json
{
  "success": true,
  "data": {
    "session_id": "f3e9c2bb-349b-4da2-8dac-c15bdfea889c",
    "question": "Is the character from a movie or TV show?",
    "guess": null,
    "confidence": 0.0,
    "question_number": 2
  }
}
```
