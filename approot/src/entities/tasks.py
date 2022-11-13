from random import uniform
from django.db.models import F
from config.celery import app
from src.entities.models import Entity
from src.core.functions import send


@app.task
def send_email_worker(user_email, pk):
    """ Celery task which calling send function. """

    send(user_email, pk)


@app.task
def increase_debt_beat():
    """ Celery task which increases Entity's debt to provider by random value in range [5, 500]. """

    for entity in Entity.objects.all():
        if entity.type == 0:
            continue

        entity.update(debt=F('debt') + round(uniform(1, 50), 2))


@app.task
def decrease_debt_beat():
    """ Celery task which decreases Entity's debt to provider by random value in range [100, 10 000]. """

    for entity in Entity.objects.all():
        if entity.type == 0:
            continue

        entity.update(debt=F('debt') - round(uniform(100, 10000), 2))

        if entity.debt < 0:
            entity.update(debt=0)
