from rest_framework import serializers
from userside.models import CustomUser,Posts

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