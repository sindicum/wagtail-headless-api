#!/bin/bash
  docker compose -f docker-compose-prod.yml exec backend python manage.py makemigrations
  docker compose -f docker-compose-prod.yml exec backend python manage.py migrate
  docker compose -f docker-compose-prod.yml exec backend python manage.py createsuperuser
  docker compose -f docker-compose-prod.yml exec backend python manage.py collectstatic --noinput