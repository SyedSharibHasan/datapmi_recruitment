
import random
import string

def generate_otp(length=6):
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))


import os
from django.core.mail import EmailMessage
from django.conf import settings


def send_otp_email(email, otp):
    subject = 'OTP verification for DataPMI Recruiter registration'
    message = f'Your OTP code is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # Create an EmailMessage object
    email_message = EmailMessage(subject, message, from_email, recipient_list)

    # Path to your image file
    image_path = '/home/user/Downloads/datapmi_recruitment/datapmiemail.png'

    # Open the image file and attach it to the email
    with open(image_path, 'rb') as image_file:
        email_message.attach('datapmiemail.png', image_file.read(), 'image/png')

    # Send the email
    email_message.send()



def send_recovery_link(email, link):
    subject = 'Password reset confirmation mail'
    message = f'Click on this link to reset your password: {link}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # Create an EmailMessage object
    email_message = EmailMessage(subject, message, from_email, recipient_list)

    # Send the email
    email_message.send()





