NAME := grhakarya
REPO_URL=https://vyavasthita.github.io/grhakarya/
BUILD_ENV ?= dev
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Welcome to $(NAME)!"
	@echo "Use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  all	run stop -> clean -> up"
	@echo "  test	run stop -> clean -> up -> runtest"
	@echo "  clean	clear network, container and images"
	@echo "  build	build container images"
	@echo "  up		run containers"
	@echo "  start	start containers"
	@echo "  restart	restart containers"
	@echo "  stop	stop containers"
	@echo "  down	bring down containers"
	@echo "  logs	show logs of containers"
	@echo "  ps		show container status"
	@echo "  destroy	destroy containers"
	@echo "  runtest	run unit tests for auth microservice"
	@echo "  u	Uninstall helm package"
	@echo "  l	Test helm menifests"
	@echo "  t	Check menifests for helm"
	@echo "  li		Install helm package from local"
	@echo "  upg	Upgrade with install helm package from local"
	@echo "  p	Create helm package"
	@echo "  ind	Create helm repo index file"
	@echo ""
	@echo "Go forth and make something great!"

ifeq ($(BUILD_ENV),test)
 $(info testing)
 ENV_FILE=configuration/environment/.env.test
 COMPOSE_FILE=docker-compose.test.yaml
else ifeq ($(BUILD_ENV), prod)
$(info production)
 ENV_FILE=configuration/environment/.env.prod
 COMPOSE_FILE=docker-compose.yaml
else
 $(info development)
 ENV_FILE=configuration/environment/.env.dev
 COMPOSE_FILE=docker-compose.yaml
endif

greet:
	@echo "Hello $(ENV_FILE)"

test: all runtest
all: stop clean up

.PHONY: clean
clean: ## clear network, container and images
	docker network prune -f
	docker container prune -f
	docker image prune -f
.PHONY: build
build: ## build container images
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) build --no-cache
.PHONY: up
up: ## run containers
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) up -d --build --remove-orphans
.PHONY: start
start: ## start containers
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) start
.PHONY: restart
restart: ## restart containers
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) stop
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) up -d
.PHONY: stop
stop: ## stop containers
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) stop
.PHONY: down
down: ## bring down containers
	docker compose down
.PHONY: logs
logs: ## show logs of containers
	docker compose logs
.PHONY: ps
ps: ## show container status
	docker ps -a
.PHONY: destroy
destroy: ## destroy containers
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) down -v
.PHONY: runtest
runtest: ## run unit tests for auth microservice
	docker compose -f $(COMPOSE_FILE) exec grahakarya-auth-test pytest /

.PHONY: u
u: ## Uninstall helm package
	helm uninstall --wait $(NAME)

.PHONY: l
l: ## Test helm menifests
	helm lint --debug --strict helm-charts/$(NAME)

.PHONY: t
t: ## Check menifests for helm
	helm template $(NAME) helm-charts/$(NAME) --debug --set global.env=$(BUILD_ENV)

.PHONY: li
li: ## Install helm package from local
	helm install $(NAME) helm-charts/$(NAME) --set global.env=$(BUILD_ENV)

.PHONY: ri
ri: ## Install helm package from remote
	helm install $(NAME) $(NAME)/$(NAME) --atomic --set global.env=$(BUILD_ENV)

.PHONY: upg
upg: ## Upgrade with install helm package from local
	helm upgrade --install --wait $(NAME) helm-charts/$(NAME) --set global.env=$(BUILD_ENV)

.PHONY: p
p: ## Create helm package
	helm package helm-charts/$(NAME) .

.PHONY: ind
ind: ## Create helm repo index file
	helm repo index . --url $(REPO_URL) --merge index.yaml .