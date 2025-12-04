from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'is_customer', 'is_agent', 'is_staff', 'is_superuser')
        read_only_fields = ('is_customer', 'is_agent')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone_number')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            is_customer=True
        )
        
        # Create Customer profile
        from customers.models import Customer
        Customer.objects.create(
            user=user,
            phone_number=validated_data.get('phone_number')
        )
        
        return user
