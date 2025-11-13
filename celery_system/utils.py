# celery_system/utils.py
from celery.result import AsyncResult
from celery_system.celery_app import app

def get_task_status(task_id: str):
    """
    获取 Celery 任务状态
    :param task_id: 任务ID
    :return: dict 包含 status, result 等
    """
    result = AsyncResult(task_id, app=app)
    
    if result.state == 'PENDING':
        return {'status': 'pending', 'task_id': task_id}
    elif result.state == 'SUCCESS':
        return {
            'status': 'success',
            'task_id': task_id,
            'result': result.result
        }
    elif result.state == 'FAILURE':
        return {
            'status': 'failure',
            'task_id': task_id,
            'error': str(result.info)
        }
    else:
        return {'status': result.state, 'task_id': task_id}


def revoke_task(task_id: str):
    """撤销任务（谨慎使用）"""
    app.control.revoke(task_id, terminate=True)
