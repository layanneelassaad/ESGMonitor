.PHONY: dev up test fmt


dev:
uvicorn backend.app:app --reload


up:
docker compose up --build


test:
pytest -q backend/tests


fmt:
ruff check --fix backend