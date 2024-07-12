from django.contrib.auth.forms import UserCreationForm 
from .models import CustomUser, BlogPost
from django import forms
class CustomSignupForm(UserCreationForm):

    #Meta class define form properties
    class Meta:
        # specify class model for this form 
        model = CustomUser
        #fields are taken from customUser model
        fields = ('first_name', 'last_name', 'profile_picture', 'username', 'email',
                    'address',
                   'city', 'state', 'pincode',"user_type")
        
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content',"draft"]


