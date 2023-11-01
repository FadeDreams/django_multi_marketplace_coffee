from django.db import models
from users.models import User, UserProfile
# from users.utils import send_notification

# Create your models here.
class Coffee(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    coffee_name = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
       return self.coffee_name 
   
