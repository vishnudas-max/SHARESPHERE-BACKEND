from django.urls import path,include
from userside import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from userside.views import PostsViewSet

router = DefaultRouter()
router.register(r'posts', PostsViewSet)

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('register/confirm/',views.RegisterConfirm.as_view()),
    path('register/resendotp/',views.ResendOtpView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('post/',views.PostCreateUpdate.as_view()),
    
]
