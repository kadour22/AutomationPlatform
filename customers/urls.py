from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from django.urls import path
from . import views
urlpatterns = [
    path("token/" , TokenObtainPairView.as_view()),
    path("refresh/" , TokenRefreshView.as_view()),
    path("dashboard/" , views.DashboardView.as_view(), name="dashboard"),
]