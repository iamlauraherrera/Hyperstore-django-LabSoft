from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField,PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from . models import Customer


class LoginForm(AuthenticationForm):
    username = UsernameField (label ='Usuario',widget=forms.TextInput(attrs= {'autofocus':'True','class':'form-control'}))
    password = forms.CharField (label='Contraseña',widget= forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control'}))


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Usuario',widget=forms.TextInput(attrs= {'autofocus':'True','class':'form-control'}))
    email = forms.EmailField(label='Correo Electronico',widget=forms.EmailInput(attrs= {'class':'form-control'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))


    class Meta:
        model = User
        fields = ['username','email','password1','password2']

#clase de cmabiar password

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Contraseña actual', widget= forms.PasswordInput(attrs= {'autofocus' : 'True','autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='Nueva contraseña', widget= forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirmar contraseña', widget= forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email= forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Nueva contraseña", widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label="Confirma la contraseña", widget=forms.PasswordInput(attrs= {'autocomplete': 'current-password','class':'form-control'}))
    

#clase para los datos del usuario
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['nombre','departamento','ciudad','direccion','telefono','codigo_postal']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.NumberInput(attrs={'class': 'form-control'}),
        }


