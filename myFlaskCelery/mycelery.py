from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('myFlaskCelery', include=['myFlaskCelery.tasks'])
app.config_from_object('myFlaskCelery.celeryconfig')

if __name__ == '__main__':
    app.start()

