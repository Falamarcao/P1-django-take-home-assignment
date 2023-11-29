dev:
	make build-dev && make up-dev


build-dev:
	docker-compose build --no-cache

up-dev: # [build-dev] must be executed before
	docker-compose up -d

# test-dev: # [up-dev or run-dev] must be executed before.
# 	docker-compose exec django python manage.py test django_food_truck.finder

stop-dev: # (optional) you can manage using the Docker Desktop GUI
	docker-compose down -v

create-conda-env: # (optional) helps code autocomplete. Conda allows to use specific python version.
	conda env create --prefix=./.env --file environment.dev.yml

update-conda-env: # (optional) Helps code autocomplete. Conda allows using a specific python version.
	conda env update --prefix=./.env --file environment.app.dev.yml --prune
