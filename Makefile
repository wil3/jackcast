dev:
	set -a && . ./.env && set +a
	flask run
.PHONY: dev

docker:
	docker-compose up --build
.PHONY: docker