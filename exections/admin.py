from django.contrib import admin

from .models import *

admin.site.register(StepExecution)
admin.site.register(WorkflowExecution)