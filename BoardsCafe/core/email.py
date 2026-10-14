from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
import logging

logger = logging.getLogger(__name__)


def send_email(subject, message, recipient_list, from_email=None, html_message=None):
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    try:
        if html_message:
            email = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipient_list,
            )
            email.attach_alternative(html_message, 'text/html')
            email.send(fail_silently=False)
        else:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        return True, None
    except Exception as e:
        logger.error(f'Failed to send email to {recipient_list}: {e}')
        return False, str(e)


def send_templated_email(template_name, context, recipient_list, from_email=None):
    from django.template.loader import render_to_string

    subject = render_to_string(f'emails/{template_name}_subject.txt', context).strip()
    text_message = render_to_string(f'emails/{template_name}.txt', context)
    html_message = render_to_string(f'emails/{template_name}.html', context)

    return send_email(subject, text_message, recipient_list, from_email, html_message)