.DEFAULT_GOAL := help .PHONY: help dev

up:
	docker compose up --build

sh:
	docker compose run web sh

migrate:
	docker compose run web flask db init
	docker compose run web flask db	migrate
	docker compose run web flask db upgrade

submit: ## Dump the Postgres database and package your project into a solution.zip file you can submit
	zip -r solution.zip .

build:
	docker compose build web --no-cache

open-app: ## Open the React app
	open http://localhost:3000




