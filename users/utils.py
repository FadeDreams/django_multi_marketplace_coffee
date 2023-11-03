from django.conf import Settings
import math
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from dotenv import load_dotenv
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.core.exceptions import ValidationError
import os
from core.settings import settings
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

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

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] # cover-image.jpg jpg is [1]
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions:' +str(valid_extensions))


def geocode_address(address):
    geolocator = Nominatim(user_agent="your_app_name")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        pass  # Handle the timeout error gracefully
    return None, None



def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    radius = 6371

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance

