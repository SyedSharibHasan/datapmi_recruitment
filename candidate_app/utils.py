
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
    subject = 'OTP Verification for DataPMI Recruiter Registration'
    html_message = render_to_string('otp_email.html', {'otp': otp})
    text_message = strip_tags(html_message)

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    email_message = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
    email_message.attach_alternative(html_message, "text/html")

    image_path = 'candidate_app/static/project_images/datapmiemail.png'
    with open(image_path, 'rb') as image_file:
        email_message.attach('datapmiemail.png', image_file.read(), 'image/png')

    email_message.send()

# def send_otp_email(email, otp):
#     subject = 'OTP Verification for DataPMI Recruiter Registration'
#     message = f'Dear User,\n\nYour One Time Password (OTP) code for verifying your email address is: \n\n<b><span style="font-size: 20px;">{otp}</span></b>.\n\nPlease use this code within the next 10 minutes to complete the registration process.\n\nPlease do not share this OTP with anyone.\n\nIf you did not request this OTP, please ignore this email.\n\nBest regards,\nDataPMI Team'
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]

#     # Create an EmailMessage object
#     email_message = EmailMessage(subject, message, from_email, recipient_list)

#     # Path to your image file
#     image_path = 'candidate_app/static/project_images/datapmiemail.png'

#     # Open the image file and attach it to the email
#     with open(image_path, 'rb') as image_file:
#         email_message.attach('datapmiemail.png', image_file.read(), 'image/png')

#     # Send the email
#     email_message.send()



# def send_recovery_link(email, link):
#     subject = 'Password reset confirmation mail'
#     message = f'Click on this link to reset your password: {link}'
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]

#     # Create an EmailMessage object
#     email_message = EmailMessage(subject, message, from_email, recipient_list)

#     # Send the email
#     email_message.send()
    
  
# def send_recovery_link(email, link):
#     subject = 'Password Reset Confirmation'
#     message = f"Hi there,\n\nA password reset for your account was requested.\n\nPlease click the link below to reset your password:\n\n{link}\n\nPlease note that this link is valid for 24 hours. After that, you will need to resubmit the request for a password reset.\n\nIf you did not request this password reset, please ignore this email.\n\nBest regards,\nYour Application Team"
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]

#     # Create an EmailMessage object
#     email_message = EmailMessage(subject, message, from_email, recipient_list)

#     # Send the email
#     email_message.send()
    
from .models import CustomUser

def send_recovery_link(email, link):
    # Fetch user object based on email
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        # Handle the case where user does not exist
        return "User not found"

    # Fetch user's name
    user_name = user.username# For full name
    # Or use: user_name = user.username  # For username

    subject = 'Password Reset Confirmation'
    message = f"Hi {user_name},\n\nA password reset for your account was requested.\n\nPlease click the link below to reset your password:\n\n{link}\n\nPlease note that this link is valid for 5 minutes. After that, you will need to resubmit the request for a password reset.\n\nIf you did not request this password reset, please ignore this email.\n\nBest regards,\nYour Application Team"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # Create an EmailMessage object
    email_message = EmailMessage(subject, message, from_email, recipient_list)

    # Send the email
    email_message.send()





# def send_notification(self, email, name):
#     subject = 'Contract Ending Notification'
#     message = f'The contract of {name} is ending in 15 days.'
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]

#     email_message = EmailMessage(subject, message, from_email, recipient_list)
#     email_message.send()





