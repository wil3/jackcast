dev:
	set -a && . ./.env && set +a
	flask run
.PHONY: dev
