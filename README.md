# una-health-test


## Tech stack used:

- Python 3.12
- Django
- Postgres DB
- Docker


## Project Setup (Local):

1) Create python virtual environment.
	```bash
	python3 -m venv .venv
	```
2) Install dependencies
	```bash
	pip install -r requirements.txt
	```
3) Create .env file in Project same as .env.template format and replace Database credentials in it.
4) Run the project
	```bash
	python manage.py runserver
	```
 
## Project Setup (Docker Compose):

1) Build
	```bash
	docker compose up --build
	```