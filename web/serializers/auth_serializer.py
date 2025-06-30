from rest_framework import serializers

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError({"email": "Field email is required"})
        if not password:
            raise serializers.ValidationError({"password": "Field password is required"})
        return data
