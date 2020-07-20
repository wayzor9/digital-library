from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms
from django.views.generic import CreateView, DeleteView

from .models import Book, Exercise


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model= User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            elif len(password1) < 8:
                raise forms.ValidationError("Password requires at least 8 characters")
        return super(RegistrationForm, self).clean(*args, **kwargs)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user doesnt exist')
            if not user.check_password(password):
                raise forms.ValidationError('The username or password was incorrect')
            if not user.is_active:
                raise forms.ValidationError('This user is active')
        return super(LoginForm, self).clean(*args, **kwargs)

class AddBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['publication_date', 'isbn']

