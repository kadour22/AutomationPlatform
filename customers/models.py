from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser) :
    ROLES_CHOICES = (
        ('owner','Owner'),
        ('admin','Admin'),
        ('manager','Manager'),
        ('employee','Employee')
    )

    role = models.CharField(max_length=100, choices=ROLES_CHOICES)

    def __str__(self):
        return self.role