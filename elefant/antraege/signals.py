from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Application


# E-Mail notifications
@receiver(post_save, sender=Application, dispatch_uid="creation_email_receiver")
def successful_application_creation(instance, created, **kwargs):
    """ Sends an e-mail to the applicant, if a new application was successfully submitted. """
    mail_from = "EleFAnt <" + settings.EMAIL_HOST_USER + ">"
    base_url = "elefant.julian-haas.de"
    url = base_url + "/" + instance.reference_number
    content_params = {'application_number': instance.application_number,
                      'reference_number': instance.reference_number,
                      'url': url}

    if created:
        send_mail(
            render_to_string('antraege/e-mails/successful_application_subject.txt'),
            # generate e-mail content using the reference number
            render_to_string('antraege/e-mails/successful_application_content.txt', content_params),
            mail_from,
            [instance.e_mail],
            fail_silently=False,
        )
