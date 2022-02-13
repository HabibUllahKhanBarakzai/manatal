start:
	docker-compose up db web
	docker-compose run --rm web python manage.py migrate

