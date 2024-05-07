# una-health-test

The Una health test application consists of three models - User, Device, and GlucoseLevel using DRF and Postgresql.

Following is the API list which sample application provides:

- POST API (api/v1/data) with reads data from csv (Try in postman which takes input as csv file)
- GET API (api/v1/levels) returns data of glucose levels in DB
- GET API (api/v1/levels/<id>) return data of glucose level of <id> specified in API


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
5) Running testcases
	```bash
	python manage.py test glucose
	```
 
## Project Setup (Docker Compose):

1) Build
	```bash
	docker compose up --build
	```
2) Migrate
	```bash
	docker exec -it <container-id> python manage.py migrate
	```