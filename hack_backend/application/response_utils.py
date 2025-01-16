from rest_framework.response import Response
from rest_framework import status

def custom_success_response(message, data=None):
    return Response({'status_code': 200,'status': 'success', 'message': message, 'data': data}, status=status.HTTP_200_OK)

def custom_error_response(message, data=None):
    return Response({'status_code': 400,'status': 'error', 'message': message, 'data': data}, status=status.HTTP_400_BAD_REQUEST)
