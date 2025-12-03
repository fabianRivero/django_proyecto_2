from django import forms
from django.contrib.auth.models import User
from profiles.models import UserProfile
from shopcart.models import Cart

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["username","email", "password"]

    def save(self):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data["password"])
        user.save()

        UserProfile.objects.create(user=user)
        Cart.objects.create(user=user)


        return user 
    
class LoginForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())