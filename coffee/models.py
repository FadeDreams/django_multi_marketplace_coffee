from django.db import models
from users.models import User, UserProfile
from users.utils import send_notification
# from users.utils import send_notification

# Create your models here.
class Coffee(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    coffee_name = models.CharField(max_length=50)
    coffee_slug = models.SlugField(max_length=100, unique=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
       return self.coffee_name 

    def save(self, *args, **kwargs):
            if self.pk is not None:
                # Update
                orig = Coffee.objects.get(pk=self.pk)
                if orig.is_approved != self.is_approved:
                    mail_template = "users/emails/admin_approval_email.html"
                    context = {
                        'user':self.user,
                        'is_approved': self.is_approved,
                    }
                    if self.is_approved == True:
                        # Send notification email
                        mail_subject = "Congratulations! Your cafe has been approved."
                        send_notification(mail_subject, mail_template, context)
                    else:
                        # Send notification email    
                        mail_subject = "We're sorry! You are not eligible for publishing your coffee menu on our marketplace"  
                        send_notification(mail_subject, mail_template, context)    
            return super(Coffee, self).save(*args, **kwargs)  
