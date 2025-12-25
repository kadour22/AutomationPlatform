from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User

class DashboardView(APIView):
    def get(self, request):
        user = request.user.role
    
        match user:
            case "owner":
                data = {
                    "message": "Welcome to the Owner Dashboard",
                }
                return Response(data, status=status.HTTP_200_OK)
         
            case "manager":
                data = {
                    "message": "Welcome to the Manager Dashboard",
                }
                return Response(data, status=status.HTTP_200_OK)
          
            case "employee":
                data = {
                    "message": "Welcome to the Employee Dashboard",
                }
                return Response(data, status=status.HTTP_200_OK)
          
            case _:
                return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)