-include .env

IMAGE = gym-project:latest
CONTAINER = gym-project
MANAGECMD = docker exec -it $(CONTAINER)
APP_LOCATION = "$(PWD)/gymproject"
DOCKERFILE = "$(PWD)/dev.Dockerfile"
HOST_PORT = $(if $(CUSTOM_HOST_PORT),$(CUSTOM_HOST_PORT),8000)

all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: delete-container ## Build the container
	@docker build --tag $(IMAGE) -f $(DOCKERFILE) $(APP_LOCATION)
	@docker run -dit --name $(CONTAINER) -v $(APP_LOCATION):/deploy -p $(HOST_PORT):8000 -w /deploy $(IMAGE) /bin/bash

test: start ## Run tests
	@$(MANAGECMD) $(DJANGO_MANAGER) test

restart: ## Restart the container
	@docker restart $(CONTAINER)

cmd: start ## Access bash
	@$(MANAGECMD) /bin/bash

up: start ## Start django server
	@$(MANAGECMD) /bin/bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"

run-celery: start ## Start processing celery queue
	@$(MANAGECMD) /bin/bash -c "celery -A gymproject.celery worker --loglevel=info -B"

start: clean
	@docker start $(CONTAINER)

down: ## Stop container
	@docker stop $(CONTAINER) || true

delete-container: down
	@docker rm $(CONTAINER) || true

remove: delete-container ## Delete containers and images
	@docker rmi $(IMAGE)

clean: ## Deletes old *.py[co] files
	@find . -name "*.py[co]" -delete

.DEFAULT_GOAL := help
