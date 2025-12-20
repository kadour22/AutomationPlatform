from django.db import models
from customers.models import User

class WorkFlow(models.Model) :
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User , on_delete=models.CASCADE , related_name='workflows')
    
    def __str__(self) :
        return self.name

class WorkFlowStep(models.Model) :

    STEPS_TYPE = (
        ('task','Task'),
        ('approval','Approval'),
        ('email','Email'),
        ('delay','Delay'),
        ('webhook','Webhook'),
    )

    workflow = models.ForeignKey(WorkFlow , on_delete=models.CASCADE , related_name='steps')
    step_type = models.CharField(max_length=100 , choices=STEPS_TYPE)
    config = models.JSONField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.workflow} {self.step_type}"