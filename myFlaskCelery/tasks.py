from __future__ import absolute_import

from myFlaskCelery.mycelery import app


@app.task
def add(x, y):
    return x+y

# from celery import Celery
# app = Celery('tasks',
#              broker='amqp://guest:guest@localhost//',
#              backend='redis://localhost:6379/0')
# @app.task
# def add(x, y):
#     return x + y

# if __name__ == '__main__':
#     add(1, 5)
