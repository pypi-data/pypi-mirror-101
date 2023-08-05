from django.core.mail import send_mail
from django.template.loader import render_to_string
from config.settings.base import ALERT_EMAIL_ADDRESSES, PROGRAM_NAME


SEND_ADDRESS = PROGRAM_NAME + ' <contact@hashtag-learning.co.uk>'

def send_user_email(user, email_id):
    subject = None

    context = {
        'user': user,
    }

    message_txt = 'pages/email/' + email_id + '.txt'
    message_html = 'pages/email/' + email_id + '.html'


    context['button_url'] = 'https://achieve.hashtag-learning.co.uk/'
    context['button_text'] = 'Launch Achieve'


    if email_id == 'evaluate-welcome':
        subject = 'Welcome to Evaluate'



    elif email_id == 'trial-expiring-today':
        subject = PROGRAM_NAME + ' free trial expiring today'
        context['button_url'] = 'https://www.hashtag-learning.co.uk/'
        context['button_text'] = 'Subscribe Now'

    elif email_id == 'trial-expired':
        subject = PROGRAM_NAME + ' free trial expired'
        context['button_url'] = 'https://www.hashtag-learning.co.uk/'
        context['button_text'] = 'Order Now'


    message = render_to_string(message_txt, context)
    html_message = render_to_string(message_html, context)


    send_address = SEND_ADDRESS

    result = send_mail(subject, message, send_address , [user.username,], html_message=html_message)

    # testing copy to MC
    """if result == 1:
        bcc_subject = 'Delivered: '+ email_id + ' to ' + user.username
    else:
        bcc_subject = 'NOT Delivered: ' + email_id + ' to ' + user.username
    send_mail(bcc_subject , message, send_address, ALERT_ADMIN_EMAIL_ADDRESSES, html_message=html_message)"""


