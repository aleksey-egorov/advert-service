from django import forms


class BrandForm(forms.Form):
    def set_initial(self, id):
        self.fields['id'].initial = id

    id = forms.IntegerField(widget=forms.HiddenInput, required=True)
    name = forms.CharField(label='Ваше имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=20)
    email = forms.EmailField(label='Email', max_length=200)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)


