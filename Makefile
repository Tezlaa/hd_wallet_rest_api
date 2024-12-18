APP_NAME = hd_wallet
APP_NAME_TEST = hd_wallet_test



build:
	@docker network create localhd_wallet || true
	@docker-compose build $(APP_NAME)

run: build
	@docker-compose up

stop:
	@docker-compose stop $(docker ps -aq)



build_test:
	@docker network create localhd_wallet_test || true
	@docker-compose -f docker-compose-test.yml build $(APP_NAME_TEST)

test: build_test
	@docker-compose -f docker-compose-test.yml run --rm $(APP_NAME_TEST) pytest tests -s -vv -ra -o console_output_style=count -k "${k}"



migrate:
	@docker-compose run --rm $(APP_NAME) alembic upgrade head

migration:
	@docker-compose run --rm $(APP_NAME) alembic revision --autogenerate -m "${name}"