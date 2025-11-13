# celery_system/config.py
import os
from env import get_env_variable

CELERY_BROKER_URL = get_env_variable('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
CELERY_RESULT_BACKEND = get_env_variable('REDIS_URL', 'redis://127.0.0.1:6379/0')

# Celery 配置字典
CELERY_CONFIG = {
    'broker_url': CELERY_BROKER_URL,
    'result_backend': CELERY_RESULT_BACKEND,
    'accept_content': ['json'],
    'task_serializer': 'json',
    'result_serializer': 'json',
    'timezone': 'Asia/Shanghai',
    'task_routes': {
        'celery_system.tasks.*': {'queue': 'ai_doctor_tasks'},
    },
}
