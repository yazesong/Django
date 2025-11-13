# celery_system/celery_app.py
import os
from celery import Celery
from celery_system.config import CELERY_CONFIG

# 设置 Django 环境（确保能访问 Django 模型）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authserver.authserver.settings')

app = Celery('ai_doctor')

app.conf.update(**CELERY_CONFIG)


app.autodiscover_tasks(['celery_system'], force=True)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
