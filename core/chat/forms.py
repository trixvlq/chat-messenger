from django import forms
from .models import ChatUser


class UserRegisterForm(forms.ModelForm):
    password_confirm = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    class Meta:
        model = ChatUser
        fields = ['username', 'email', 'password','password_confirm', 'name', 'surname', 'nickname', 'pfp']
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
