from django.db import models
from customers.models import User

class Task(models.Model) :
    title   = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(
        User , on_delete=models.CASCADE , related_name='tasks'
    )

    created_at = models.DateTimeField(
        auto_now_add=True , null=True
    )

    def __str__(self) :
        return self.title