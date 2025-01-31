from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'password', 'mobile', 'email', 'answer']
        extra_kwargs = {
            'password': {'write_only': True}
        }
