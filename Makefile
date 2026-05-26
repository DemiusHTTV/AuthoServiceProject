up:
	docker-compose up -d --build

down:
	docker-compose down

ps:
	docker-compose ps

logs-auto:
	docker-compose logs -f autoservices

logs-wh:
	docker-compose logs -f warehouse
