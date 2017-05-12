from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from .models import Application


# E-Mail notifications
# noinspection PyUnusedLocal
@receiver(post_save, sender=Application, dispatch_uid="creation_email_receiver")
def successful_application_creation(instance, created, **kwargs):
    """ Sends an e-mail to the applicant, if a new application was successfully submitted. """
    mail_from = "eleFant <" + settings.EMAIL_HOST_USER + ">"
    base_url = settings.ALLOWED_HOSTS[0]
    url = "http://" + base_url + reverse('elefant:detail', args=[str(instance.pk)])
    content_params = {'application_number': str(instance.application_number),
                      'reference_number': str(instance.reference_number),
                      'url': url}

    if created:
        send_mail(
            render_to_string('elefant/e-mails/successful_application_subject.txt'),
            # generate e-mail content using the reference number
            render_to_string('elefant/e-mails/successful_application_content.txt', content_params),
            mail_from,
            [instance.e_mail],
            fail_silently=False,
        )
