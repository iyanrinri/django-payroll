from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Email is already in use")
        return value

    @staticmethod
    def validate_role(value):
        if value != 'EMPLOYEE':
            raise serializers.ValidationError("Role must be 'EMPLOYEE'")
        return value

    def validate(self, data):
        name = data.get('name')
        if not name:
            raise serializers.ValidationError({"name": "Field Name is required"})
        if len(name) > 100:
            raise serializers.ValidationError({"name": "Field Name is required"})

        email = data.get('email')
        if not email:
            raise serializers.ValidationError({"email": "Field email is required"})
        if len(email) > 255:
            raise serializers.ValidationError({"email": "Field email length must not exceed 255 characters"})

        if self.context['request'].method == 'POST' and 'role' not in data:
            data['role'] = 'EMPLOYEE'

        return data