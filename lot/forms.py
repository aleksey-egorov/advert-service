from django import forms

from utils.form import FormHelper


class FilterForm(forms.Form):

    def __init__(self, regions, categories, groups, brands):
        super().__init__()
        self.regions = regions
        self.categories = categories
        self.groups = groups
        self.brands = brands

    def set_options(self, params):
        self.fields['region'].choices = FormHelper.make_options(self.regions)
        self.fields['category'].choices = FormHelper.make_options(self.categories)
        self.fields['group'].choices = FormHelper.make_options(self.groups)
        self.fields['brand'].choices = FormHelper.make_options(self.brands)

        self.fields['region'].initial = params['region']
        self.fields['category'].initial = params['category']
        self.fields['group'].initial = params['group']

    page = forms.IntegerField(widget=forms.HiddenInput, required=False)
    region = forms.ChoiceField(label='Регион')
    category = forms.ChoiceField(label='Категория')
    group = forms.ChoiceField(label='Группа')
    brand = forms.MultipleChoiceField(label='Производитель')

    #TODO: add extra fields and validation

    #def clean_login(self):
    #    login = self.cleaned_data['login']
    #    if User.objects.filter(username=login).exists():
    #        raise forms.ValidationError('User with login "' + login+ '" already exists')
    #    return login




