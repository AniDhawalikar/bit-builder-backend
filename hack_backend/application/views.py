from django.http import JsonResponse
import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Customer
from .serializers import CustomerSerializer
from .response_utils import custom_success_response, custom_error_response
# Token validation decorator
from functools import wraps
from django.http import JsonResponse
 

def token_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        request = args[1]
        token = request.headers.get('Authorization')
        if not token:
            return custom_error_response('Token is missing.')
        # print(f"Authorization Header: {token}")
        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]  # Remove "Bearer"
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = Customer.objects.get(id=decoded_token['id'], token=token)
            request.user = user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Customer.DoesNotExist):
            return custom_error_response('Invalid or expired token.')
        return view_func(*args, **kwargs)
    return wrapped_view


def sample_get_api(request):
    if request.method == "GET":
        data = {
            "message": "Hello, this is a simple GET API!",
            "status": "success"
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return custom_success_response('User registered successfully.')
        return custom_error_response('Invalid data.', serializer.errors)


class SignInWithTokenAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            # Retrieve the customer
            customer = Customer.objects.get(email=email)
            
            # Check password
            if check_password(password, customer.password):
                # Generate a token
                token = jwt.encode({'id': customer.id, 'email': customer.email}, settings.SECRET_KEY, algorithm="HS256")
                customer.token = token
                customer.save()
                return custom_success_response('Logged in successfully.', {'token': token})
            
            # If password does not match
            return custom_error_response('Invalid credentials.')
        except Customer.DoesNotExist:
            # If customer does not exist
            return custom_error_response('Invalid credentials.')


class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        answer = request.data.get('answer')
        new_password = request.data.get('new_password')

        if not email or not answer or not new_password:
            return custom_error_response('Email, new_password and answer are required.')

        try:
            user = Customer.objects.get(email=email)
            # Check if the provided current password is correct
            # current_password = user.password
            # if check_password(current_password, user.password):
                # Check if the new password is the same as the current password
                # if check_password(new_password, user.password):
                #     return custom_error_response('New password cannot be the same as the current password.')
            # Hash the new password and save it
            if user.answer == answer:
                user.password = make_password(new_password)
                user.save()
                return custom_success_response('Password updated successfully.')
            else:
                return custom_error_response('Incorrect Answer.')
        except Customer.DoesNotExist:
            return custom_error_response('User not found.')


class LogoutAPIView(APIView):
    @token_required
    def post(self, request):
        email = request.data.get('email')
        user = Customer.objects.get(email=email)
        if user:
            user.token = None
            user.save()
            return custom_success_response('Logged out successfully.')
        else:
            return custom_error_response('user not found')
