from tasks import cooking_task
from tasks import get_faculty
from celery import Celery
import os
import time

# for i in range(8):
#     result = cooking_task.delay(i)
#     print(result)

# n = os.popen('redis/redis-stable/src/redis-cli -h localhost -p 6379 -n 0 llen celery').read()
# print(n)

# t = 12
# while True:
#     n = os.popen('redis/redis-stable/src/redis-cli -h localhost -p 6379 -n 0 llen celery').read()
#     if int(n) < 6:
#         for _ in range(10):
#             result = cooking_task.delay(t)
#             print(result)
#             t += 1
#     time.sleep(8)




for i in range(8):
    result = get_faculty.delay('uiuc', 'cs')
    print(result)

n = os.popen('redis/redis-stable/src/redis-cli -h localhost -p 6379 -n 0 llen celery').read()
print(n)

while True:
    n = os.popen('redis/redis-stable/src/redis-cli -h localhost -p 6379 -n 0 llen celery').read()
    if int(n) < 6:
        for _ in range(10):
            result = get_faculty.delay('uiuc', 'cs')
            print(result)
    time.sleep(8)
