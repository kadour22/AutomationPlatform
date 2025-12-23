from django.db import models
from typing import Dict, Any , Optional

class WorkflowExecution(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("running", "Running"),
        ("paused", "Paused"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    workflow = models.ForeignKey(
        "workflows.Workflow",
        on_delete=models.CASCADE
    )
    triggered_by = models.ForeignKey(
        "customers.User",
        null=True,
        on_delete=models.SET_NULL
    )
    status   = models.CharField(max_length=20, choices=STATUS_CHOICES)
    context   = models.JSONField()
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta :
        ordering = ['-started_at']
    
    def initialize_context(self, inputs:Dict[str, Any] , metadata: Optional[Dict[str, Any]] = None):
        self.context = {
            "schema_version" : "1.0" , 
            "inputs":inputs , 
            "vacriables" : {} , 
            "metadata" : {
                "workflow_version" : getattr(self.workflow , 'version' , '1.0')
            },
            "state" : {
                "current_step":None , 
                "completed_step":[] , 
                "failed_step":[] ,
                "skipped_step":[] , 
            }
        }
        self.save()
        # return self.context

    


class StepExecution(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("running", "Running"),
        ("waiting", "Waiting"),
        ("done", "Done"),
        ("error", "Error"),
    )

    workflow_execution = models.ForeignKey(
        WorkflowExecution,
        related_name="steps",
        on_delete=models.CASCADE
    )
    step = models.ForeignKey(
        "workflows.WorkflowStep",
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    output = models.JSONField(null=True, blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    def start(self):
        """Mark the step as running."""
        self.status = "running"
        self.save(update_fields=['status'])