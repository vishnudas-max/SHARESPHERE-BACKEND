from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,PostsSerializer,postCreateSeializer
import pyotp
import time
from .models import Regotp
import time
from .tasks import send_mail_to
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser,Posts
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
# Create your views here.




class RegisterView(APIView):

    def generate_otp(self):
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret,interval=120,digits= 4)
        otp = totp.now()
        return otp,secret

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            request.session['userdata'] = data
            otp,secret = self.generate_otp()
            email = data['email']
            message = f"""
                        SHARESPHERE,
                           Your OTP for Verification {otp}
                    """
            title = "OTP VERIFICATION"
            # sending mail-
            send_mail_to.delay(message=message,mail=email)
            # saving the otp-
            obj,created =Regotp.objects.update_or_create(
                email = email,
                defaults={
                    'secret':secret,
                    'user_data':data
                }
            )
           
            return Response({'status': True, 'message': 'OTP sent','email':email}, status=status.HTTP_200_OK)
        
        return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RegisterConfirm(APIView):

    def post(self, request):
        otp = request.data['otp']
        email =request.data['email']
        try:
            obj = Regotp.objects.values('secret','user_data','otp_time').get(email=email)
            secret = obj['secret']
            user_data = obj['user_data']
            totp = pyotp.TOTP(secret,interval=120,digits= 4)
            is_valid = totp.verify(otp)
            print(is_valid)
        except:
            return Response({'status':False,'message':'request time out'},status= status.HTTP_400_BAD_REQUEST)
    
        if is_valid:
            serializer = RegisterSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                Regotp.objects.get(email=email).delete()
                return Response({'status': True, 'message': 'user created '},status=status.HTTP_201_CREATED)
        else:
            current_time = timezone.now()
            time_difference = current_time - obj['otp_time']
            if time_difference > timedelta(minutes=2):
                return Response({'status': False, 'message': 'Otp time out'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': False, 'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class ResendOtpView(APIView):

    def post(self,request):
        try:
            email = request.data['email']
            obj = Regotp.objects.get(email=email)
            secret = obj.secret
        except:
            return Response({'status':False,'message':'Request time out'},status=status.HTTP_400_BAD_REQUEST)
        totp = pyotp.TOTP(secret,interval=120,digits= 4)
        otp = totp.now()
        Regotp.objects.filter(email=email).update(otp_time=timezone.now())
        message = f"""
                        SHARESPHERE,
                           Your OTP for Verification {otp}
                    """
        title = "OTP VERIFICATION"
            # sending mail-
        send_mail_to.delay(message=message,mail=email)
        
        return Response({'status':True,'message':'OTP send','email':email},status=status.HTTP_200_OK)


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

