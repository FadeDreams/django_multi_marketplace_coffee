from django.conf import Settings
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from dotenv import load_dotenv
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from core.settings import  settings
load_dotenv()

def check_coffee_role(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_customer_role(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'coffeeDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'userDashboard'
        return redirectUrl
    elif user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl


def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    # current_site = 'xxx'
    
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        # 'uid': urlsafe_base64_encode(force_bytes(user)),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        # 'token': 'sss',
    })
    to_email = user.email
    # to_email = SETTINGS.TESTEMAIL1
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
    
    
def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context['user'].email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()

def sendemail():
    mail_subject = 'Please activate your account'
    email_template = 'users/emails/account_verification_email.html'
    send_verification_email("xxx", settings.TESTEMAIL1 , mail_subject, email_template)
