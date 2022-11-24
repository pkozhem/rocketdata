from random import uniform
from django.db.models import F
from config.celery import app
from src.entities.models import Entity
from src.core.functions import send


@app.task
def send_email_worker(user_email, pk) -> None:
    """ Celery task which calling send function. """

    send(user_email, pk)


@app.task
def increase_debt_beat() -> None:
    """
    Celery task which increases Entity's debt to provider by random value in range [5, 500].
    Calling every 3 hours starting from midnight.
    """

    Entity.objects.exclude(type=0).update(debt=F('debt') + round(uniform(1, 50), 2))


@app.task
def decrease_debt_beat() -> None:
    """
    Celery task which decreases Entity's debt to provider by random value in range [100, 10 000].
    Calling daily at 6:30 AM.
    """

    entities = Entity.objects.exclude(type=0)
    entities.update(debt=F('debt') - round(uniform(100, 10000), 2))
    entities.filter(debt__lt=0).update(debt=0)


@app.task
def make_debt_zero_worker(instance_id_and_debt) -> None:
    """ Updates Entities' debts to zero. """

    for details in instance_id_and_debt:
        for entity_id in details.values():
            Entity.objects.filter(id=entity_id).update(debt=0.00)
