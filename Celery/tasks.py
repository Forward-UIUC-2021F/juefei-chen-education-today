# celery -A tasks worker --pool=solo --loglevel=info
# celery -A tasks worker --pool=prefork --concurrency=4 --loglevel=info
# src/redis-server --protected-mode no

# redis/redis-stable/src/redis-cli -h localhost -p 6379 -n 0 llen celery

# we are importing Celery class from celery package
from celery import Celery
import time
# from algorithm import find

# Redis broker URL
# BROKER_URL = 'redis://localhost:6379/0'
BROKER_URL = 'redis://juefeic2@172.22.224.119:6379/0'

# We are creating an instance of Celery class by passing module name as Restaurant and broker as Redis.
celery_app = Celery('Restaurant', broker=BROKER_URL)

# we are decorating cooking_task function with @celery_app.task decorator.
# Functions which are decorated with @celery_app.task considered celery tasks.
@celery_app.task
def cooking_task(n):
    time.sleep(5)
    print(n)

# @celery_app.task
# def get_faculty(university, department):
#     data, url = find(university, department)
#     print('fs', url)