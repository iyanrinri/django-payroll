import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payroll_web.settings")

app = Celery("payroll_web")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
