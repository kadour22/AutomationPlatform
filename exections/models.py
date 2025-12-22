from django.db import models

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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    context = models.JSONField()
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

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
