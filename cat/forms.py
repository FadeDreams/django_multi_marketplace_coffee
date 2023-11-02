# mail.mime import image
from django import forms
from users.utils import allow_only_images_validator
from .models import Category, CoffeeItem

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']
        
        
class CoffeeItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    class Meta:
        model = CoffeeItem
        fields = ['category', 'coffee_name', 'description', 'price', 'image', 'is_available']
    
