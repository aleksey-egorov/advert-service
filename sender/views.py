from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings

from brand.models import Brand
from brand.forms import BrandForm
from sender.const import EMAIL_TEMPLATES
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