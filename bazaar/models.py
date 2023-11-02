from unittest.util import _MAX_LENGTH
from django.db import models
from users.models import User
from cat.models import CoffeeItem

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coffeeitem = models.ForeignKey(CoffeeItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.user
    
