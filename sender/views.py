from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings

from brand.models import Brand
from brand.forms import BrandForm
from supplier.models import Supplier, SupplierOrg
from supplier.forms import SupplierOrgContactForm, SupplierContactForm
from utils.mailer import Mailer

# Create your views here.

class BrandSendMessageView(View):
    ''' '''
    def post(self, request):
        form = BrandForm(request.POST)
        if form.is_valid():
            brand_id = int(form.cleaned_data['id'])
            brand = Brand.objects.get(id=brand_id)

            message_context = {
                'name': form.cleaned_data['name'],
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message']
            }
            subject = 'Помощь в подборе ' + brand.name
            result = Mailer().send_template_message([settings.EMAIL_TO], 'brand_message',
                                                    subject, message_context)
            return JsonResponse({'result': result}, safe=False)


class SupplierOrgSendMessageView(View):
    ''' '''
    def post(self, request):
        form = SupplierOrgContactForm(request.POST)
        if form.is_valid():
            suporg_id = int(form.cleaned_data['id'])
            suporg = SupplierOrg.objects.get(id=suporg_id)

            message_context = {
                'name': form.cleaned_data['name'],
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message']
            }

            subject = 'Cообщение для постащика ' + suporg.name
            result = Mailer().send_template_message([settings.EMAIL_TO], 'supplier_message',
                                                    subject, message_context)
            return JsonResponse({'result': result}, safe=False)


class SupplierSendMessageView(View):
    ''' '''
    def post(self, request):
        form = SupplierContactForm(request.POST)
        if form.is_valid():
            supplier_id = int(form.cleaned_data['id'])
            supplier = Supplier.objects.get(id=supplier_id)

            message_context = {
                'name': form.cleaned_data['name'],
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message']
            }

            subject = 'Cообщение для постащика ' + supplier.full_name
            result = Mailer().send_template_message([settings.EMAIL_TO], 'supplier_message',
                                                    subject, message_context)
            return JsonResponse({'result': result}, safe=False)