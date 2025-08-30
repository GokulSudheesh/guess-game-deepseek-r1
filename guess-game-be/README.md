### Setting up Backend Development Environment

- Run redis locally

  ```bash
  docker compose up redis
  ```

- Install the required packages with poetry:

  ```bash
  poetry install
  poetry run uvicorn app.main:app
  ```
