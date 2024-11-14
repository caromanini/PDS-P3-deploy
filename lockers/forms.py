# lockers/forms.py
from django import forms
from .models import Locker

class LockerPasswordForm(forms.ModelForm):
    password = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={'type': 'password', 'pattern': '[1-6]{4}', 'title': 'Ingrese solo números del 1 al 6'})
    )
    
    class Meta:
        model = Locker
        fields = ['password']
        
class LockerEmailForm(forms.ModelForm):
    owner_email = forms.EmailField(label="Nuevo Correo Electrónico")

    class Meta:
        model = Locker
        fields = ['owner_email']