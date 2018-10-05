from django import forms
from user.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','avatar',)


class RegisterForm(forms.Form):
    class Meta:
        model = User

    login = forms.CharField(label='Логин', max_length=200)
    email = forms.EmailField(label='E-mail', max_length=200)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', max_length=200)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Пароль (повтор)', max_length=200)
    avatar = forms.ImageField(label='Аватар')

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(username=login).exists():
            raise forms.ValidationError('Пользователь с логином "' + login+ '" уже существует')
        return login

