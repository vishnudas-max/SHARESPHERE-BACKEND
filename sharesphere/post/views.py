from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .serializers import postCreateSeializer,PostsSerializer
from userside.models import Posts
from rest_framework.views import APIView


# Create your views here.


class PostsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes =[IsAuthenticated]
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    @action(detail=False, methods=['get'], url_path='user-post/(?P<user_id>[^/.]+)')
    def user_posts(self, request, user_id=None):
        posts = Posts.objects.filter(userID=user_id)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(is_deleted=False)
        return query_set
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)




class PostCreateUpdate(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes =[IsAuthenticated]
    
    def post(self,request):
        data = request.data
        serializer = postCreateSeializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
        data = request.data
        obj = Posts.objects.get(id = data['id'])
        serializer = PostsSerializer(obj,data=data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'message':'Post Updated'},status=status.HTTP_200_OK)
        return Response({'status':False},serializer.errors,status=status.HTTP_400_BAD_REQUEST)

