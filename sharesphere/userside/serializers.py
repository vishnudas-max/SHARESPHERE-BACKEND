from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Posts


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['is_admin'] = user.is_superuser
 

        return token

class RegisterSerializer(serializers.Serializer):


    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,data):
        if data['username']:
            if CustomUser.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('Username already in use!')
        if data['email']:
            if CustomUser.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('Email already in use !')
            
        return data

    def create(self,validated_data):
        print(validated_data)
        user = CustomUser.objects.create(username = validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return validated_data


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username']

class PostsSerializer(serializers.ModelSerializer):
    userID = UserDetailsSerializer(read_only=True)
    
    class Meta:
        model = Posts
        fields = ['id','userID', 'caption', 'contend', 'uploadDate', 'updatedDate', 'is_deleted']

class postCreateSeializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['userID','caption','contend']