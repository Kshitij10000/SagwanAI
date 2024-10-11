# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hello.settings')

app = Celery('Hello')

# Use Django's settings, with a 'CELERY' namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Define task routes if necessary
app.conf.task_routes = {
    'Home.tasks.process_stock_data': {'queue': 'process_stock_data'},
    'Home.tasks.fetch_live_ticker_data': {'queue': 'fetch_live_ticker_data'},
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
