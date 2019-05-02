from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
