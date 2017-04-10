from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Application

SUBJECT = "Erfolg!"
FROM = "EleFAnt <elefant@julian-haas.de>"


def successful_application_mail_content(application_number, reference_number, url):
    return "Dein Finanzantrag wurde erfolgreich gestellt! \n" \
           "\n" \
           "FA-Nummer: " + application_number + "\n" \
           "Referenznummer: " + reference_number + "\n" \
           "\n" \
           "Unter folgendem Link kannst du den aktuellen Status abfragen: " + url + \
           "\n\n" + \
           "Viele Grüße \n" + \
           "Dein EleFAnt"


# E-Mail notifications
@receiver(post_save, sender=Application, dispatch_uid="creation_email_receiver")
def send_email_upon_application_creation(sender, instance, created, **kwargs):
    """ Sends an e-mail to the applicant, if a new application was successfully submitted. """
    if created:
        send_mail(
            SUBJECT,
            # generate e-mail content using the reference number
            successful_application_mail_content(
                str(instance.application_number), str(instance.reference_number), str(instance.reference_number)),
            FROM,
            [instance.e_mail],
            fail_silently=False,
        )
