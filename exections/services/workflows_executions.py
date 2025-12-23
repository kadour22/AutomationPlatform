from exections.models import WorkflowExecution , StepExecution


"""
 step 1: create workflow execution (status running) 
        --> create step execution(status pending ==> running ) 
        --> 

"""

def email_workflow_execuction(step_execution) :
    print("email workflow")

def approval_workflow_execuction(step_execution) :
    print("approval")

def webhook_workflow_execuction(step_execution) :
    print("webhook")

def task_workflow_execuction(step_execution) :
    print("task")