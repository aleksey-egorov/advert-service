from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=20)
    email = forms.EmailField(label='Email', max_length=200)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)


