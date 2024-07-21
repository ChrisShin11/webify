from celery import Celery
from app.config import settings

celery_app = Celery(
    'webify',
    broker=settings.CELERY_BROKER_URL,
    include=['app.services.document_processor']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task
def process_document_task(file_path: str):
    from app.services.document_processor import document_processor
    document_processor.process_document(file_path)