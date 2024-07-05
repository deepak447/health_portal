from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomSignupForm(UserCreationForm):

    #Meta class define form properties
    class Meta:
        # specify class model for this form 
        model = CustomUser
        #fields are taken from customUser model
        fields = ('first_name', 'last_name', 'profile_picture', 'username', 'email',
                    'address',
                   'city', 'state', 'pincode',"user_type")



