from django.template.loader import render_to_string
from django.core.mail import EmailMessage


# def send_html_email(template, context, subject, from_email, to_email):
#     # import html message.html file
    
#     # message = render_to_string(template, {'context': context, })
#     message = render_to_string(template, context)

#     message = EmailMessage(subject, message, from_email, [to_email])
#     # this is required because there is no plain text email message
#     message.content_subtype = 'html'
#     message.send()


def send_html_email(subject_template, subject_context, body_template, body_context, from_email, to_email):
    subject = render_to_string(subject_template, subject_context)
    subject = ''.join(subject.splitlines()).strip()
    body = render_to_string(body_template, body_context)
    message = EmailMessage(subject, body, from_email, [to_email])
    message.content_subtype = 'html'
    message.send()
