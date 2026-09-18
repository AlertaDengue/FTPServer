COMPOSE ?= docker compose
COMPOSE_FILES := -f docker-compose.yaml -f docker-compose.dev.yaml

.PHONY: up down

up:
	$(COMPOSE) $(COMPOSE_FILES) up --build --force-recreate --remove-orphans -d

down:
	$(COMPOSE) $(COMPOSE_FILES) down --remove-orphans