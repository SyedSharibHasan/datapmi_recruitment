
import random
import string

def generate_otp(length=6):
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))


import os
from django.core.mail import EmailMessage
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_otp_email(email, otp):
    subject = 'OTP Verification for DataPMI Registration'
    html_message = render_to_string('otp_email.html', {'otp': otp})
    text_message = strip_tags(html_message)

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    email_message = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
    email_message.attach_alternative(html_message, "text/html")

    email_message.send()


    
from .models import CustomUser

def send_recovery_link(email, link):
    # Fetch user object based on email
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        # Handle the case where user does not exist
        return "User not found"

    user_name = user.username
    subject = 'Password Reset Confirmation'
    
    # Pass context data as a single dictionary
    context = {'link': link, 'user': user_name}
    
    # Render HTML message using the template and context data
    html_message = render_to_string('reset_link.html', context)
    
    # Create plain text version of the HTML email
    text_message = strip_tags(html_message)
    
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    email_message = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
    email_message.attach_alternative(html_message, "text/html")

    email_message.send()


