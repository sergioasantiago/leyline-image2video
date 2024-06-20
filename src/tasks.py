import shutil
import os
import uuid

from celery import Celery
from time import sleep

CELERY_BROKER_URL = 'redis://redis:6379/0',
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
SLEEP_TIME_SECONDS = 30
GENERATED_FOLDER = '/data/generated/'
EXAMPLE_VIDEO = '/tmp/video.mp4'

celery = Celery(
    'celery',
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL
)


def generate_video(image_path):
    # Simulate video generation
    video_name = f'{uuid.uuid4()}.mp4'
    video_path = os.path.join(GENERATED_FOLDER, video_name)
    shutil.copy(EXAMPLE_VIDEO, video_path)
    return video_name


@celery.task(bind=True)
def process_image(self, image_path):
    self.update_state(state='PROCESSING', meta={'progress': 0})

    # Simulate video generation
    for i in range(SLEEP_TIME_SECONDS):
        progress = f"{int(i * 100 / SLEEP_TIME_SECONDS)}%"
        self.update_state(state='PROCESSING', meta={'progress': progress})
        sleep(1)

    return {'video_url': generate_video(image_path)}
