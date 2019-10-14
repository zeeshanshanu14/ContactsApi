from celery.schedules import timedelta

CELERY_IMPORTS = ('automated_tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'create_contact':
        {
            'task': 'automated_tasks.create_random_contact_15sec',
            'schedule': timedelta(seconds=15),
        },
    'delete_contact':
        {
            'task': 'automated_tasks.delete_task_older_1min',
            'schedule': timedelta(minutes=1),
        }
}
