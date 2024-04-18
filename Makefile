.PHONY: install_packages
install_packages:
	poetry install

.PHONY: flake
flake:
	poetry run flake8

.PHONY: runserver
runserver:
	poetry run python3 manage.py runserver 0.0.0.0:3030

.PHONY: makemigrations
makemigrations:
	poetry run python3 manage.py makemigrations

.PHONY: migrate
migrate:
	poetry run python3 manage.py migrate

.PHONY: shell
shell:
	poetry run python3 manage.py shell

.PHONY: startapp
startapp:
	poetry run python3 manage.py startapp $(app)

.PHONY: seedsuperadmin
seedsuperadmin:
	poetry run python3 manage.py seed_admin

.PHONY: createsuperuser
createsuperuser:
	poetry run python3 manage.py createsuperuser

.PHONY: project_setup
project_setup: install_packages makemigrations migrate seedsuperadmin;
	