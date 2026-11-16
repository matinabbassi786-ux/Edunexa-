from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True)
def test_task(self, names):
  logger.info("Edunexa Background Task Working!")
  logger.info(names)
  return "SUCCESS"