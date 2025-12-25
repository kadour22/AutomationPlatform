from django.db import models
from customers.models import User

class Approval(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    approved  = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Approval(requester={self.requester}, approved={self.approved})"