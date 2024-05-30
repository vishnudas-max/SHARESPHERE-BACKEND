from django.db import models
from userside.models import CustomUser,Posts
# Create your models here.


class PostLike(models.Model):
    userID = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='likedpost')
    postID = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='postlikes')