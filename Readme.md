1) create db
python migrate db init
python migrate db migrate
python migrate db upgrade

I used postman to interact with endpoints

for scehduled tasks start redis locally
then

celery worker -b redis://localhost:6379 --app=run.celery -l INFO
celery beat -A run.celery --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid
