# celery_system/tasks.py
from celery import shared_task
import logging
import os
from django.conf import settings
from ppt_docx.ppt_generation import generate_ppt_from_content
from ppt_docx.docx_generation import generate_docx_from_content
from rag.rag_chain import rebuild_user_vectorstore
from audio.audio_generate import text_to_speech_file

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def async_generate_ppt(self, user_id: str, topic: str, content: str):
    """
    异步生成 PPT
    :param user_id: 用户ID
    :param topic: PPT主题
    :param content: 内容大纲
    :return: 文件路径或错误信息
    """
    try:
        # 确保用户目录存在
        user_dir = os.path.join(settings.MEDIA_ROOT, 'user_data', user_id, 'generated')
        os.makedirs(user_dir, exist_ok=True)
        
        file_path = generate_ppt_from_content(topic, content, output_dir=user_dir)
        return {
            "status": "success",
            "file_path": file_path,
            "download_url": f"/media/user_data/{user_id}/generated/{os.path.basename(file_path)}"
        }
    except Exception as exc:
        logger.error(f"PPT 生成失败 (user={user_id}): {str(exc)}")
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=2)
def async_generate_docx(self, user_id: str, title: str, content: str):
    """异步生成 Word 文档"""
    try:
        user_dir = os.path.join(settings.MEDIA_ROOT, 'user_data', user_id, 'generated')
        os.makedirs(user_dir, exist_ok=True)
        
        file_path = generate_docx_from_content(title, content, output_dir=user_dir)
        return {
            "status": "success",
            "file_path": file_path,
            "download_url": f"/media/user_data/{user_id}/generated/{os.path.basename(file_path)}"
        }
    except Exception as exc:
        logger.error(f"Word 生成失败 (user={user_id}): {str(exc)}")
        raise self.retry(exc=exc)


@shared_task
def async_rebuild_rag_index(user_id: str):
    """异步重建用户知识库向量索引"""
    try:
        rebuild_user_vectorstore(user_id)
        return {"status": "success", "user_id": user_id}
    except Exception as exc:
        logger.error(f"RAG 重建失败 (user={user_id}): {str(exc)}")
        raise


@shared_task
def async_text_to_speech(user_id: str, text: str, lang: str = "zh-CN"):
    """异步语音合成"""
    try:
        user_dir = os.path.join(settings.MEDIA_ROOT, 'user_data', user_id, 'audio')
        os.makedirs(user_dir, exist_ok=True)
        
        audio_path = text_to_speech_file(text, output_dir=user_dir, lang=lang)
        return {
            "status": "success",
            "audio_path": audio_path,
            "audio_url": f"/media/user_data/{user_id}/audio/{os.path.basename(audio_path)}"
        }
    except Exception as exc:
        logger.error(f"TTS 失败 (user={user_id}): {str(exc)}")
        raise
