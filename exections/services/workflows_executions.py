from django.core.mail import send_mail
from django.conf import settings

def email_workflow_execuction(to) :
    subject = "automation test"
    message = "welcome to our platform"
    from_email = settings.EMAIL_HOST_USER 
    recipient_list = [to] 
    send_mail(
        subject , message , from_email , recipient_list
    )
    print(f"email sent to {to}")
def approval_workflow_execuction(step_execution) :
    print("approval")

def webhook_workflow_execuction(step_execution) :
    print("webhook")

def task_workflow_execuction(step_execution) :
    print("task")