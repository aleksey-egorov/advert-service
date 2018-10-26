import re
import logging

from django.core.mail import send_mail
from django.conf import settings
from sender.const import EMAIL_TEMPLATES, EMAIL_SIGN

class Mailer():
    logger = logging.getLogger('advert.mailer')

    def send_template_message(self, email, alias, subject=None, context=None):
        try:
            msg = EMAIL_TEMPLATES[alias]
            if subject == None:
                subject = msg[0]
            message = self.replace_context(msg[1], context) + EMAIL_SIGN
            send_mail(subject, message=' ', html_message=message,
                from_email=settings.EMAIL_FROM, recipient_list=email,
                fail_silently=False,
            )
            return True
        except Exception as err:
            self.logger.error(err)

    def replace_context(self, msg, context):
        if isinstance(context, dict):
            for key in context.keys():
                tag = '<%' + str(key).upper() + '%>'
                msg = re.sub(tag, context[key], msg)

        return msg

    def send_message(self, email_to, email_from, subject, message):
        try:
            send_mail(subject, message=' ', html_message=message,
                from_email=email_from, recipient_list=[email_to],
                fail_silently=False,
            )
            return True
        except Exception as err:
            self.logger.error(err)