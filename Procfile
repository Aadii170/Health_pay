web: daphne -b 0.0.0.0 -p $PORT hospitalmanagement.asgi:application

# Optional release step to run migrations and collect static files automatically
release: python manage.py migrate && python manage.py collectstatic --noinput
