
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workflows/' , include('workflows.urls')),
    path('executions/' , include('exections.urls')),
    path('customers/' , include('customers.urls')),
]
