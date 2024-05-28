from rest_framework import serializers
from userside.models import CustomUser


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'