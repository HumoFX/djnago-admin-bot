echo "Collect static files"
python3 manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
#python manage.py makemigrations
python3 manage.py migrate
# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8001
#gunicorn -b 0.0.0.0:8001 edubookBot
#python3 manage.py botpolling --username=edubooksbot

