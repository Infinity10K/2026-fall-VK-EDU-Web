from django import forms
from django.contrib.auth.models import User

from qna.models import ImageModel


class LoginForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username == password:
            raise forms.ValidationError('Username and password same')

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if username == 'test':
            raise forms.ValidationError('Test user error')

        return username

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.startswith('admin'):
            raise forms.ValidationError('Admin user error')
        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data

    def save(self, commit=True):
        # user = User(**self.cleaned_data)
        # # username='test', email='te@tet.com', password='test'
        # user = super().save(commit=False)
        # user.set_password(self.cleaned_data['password'])
        # user.save()
        self.cleaned_data.pop('password2')
        user = User.objects.create_user(**self.cleaned_data)
        return user

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ('title', 'image')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        image = super().save(commit=False)
        image.user = self._user
        image.save()
        return image
