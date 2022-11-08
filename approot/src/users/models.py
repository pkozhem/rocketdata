from django.db import models
from django.contrib.auth.models import AbstractUser
from src.entities.models import Entity


class User(AbstractUser):
    """ Default User model inherited from Django's Abstract User model. """

    entity = models.ForeignKey(Entity, related_name='user', null=True, blank=True, on_delete=models.SET_NULL)
    pass

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
