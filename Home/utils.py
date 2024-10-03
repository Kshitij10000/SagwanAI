from django.core.mail import send_mail
from django.conf import settings

def send_email_to_user():
    subject = "testmail"
    message = "testing it"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['kshitijsarve2001@gmail.com']
    send_mail(subject,message,from_email,recipient_list)