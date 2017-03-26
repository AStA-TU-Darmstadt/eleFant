from django.db import models


class Application(models.Model):  # Finanzantrag
    applicant = models.CharField(max_length=100)  # Antragsteller*in
    number = models.CharField(primary_key=True, max_length=20)  # FA-Nummer
    application_date = models.DateTimeField('date of application')  # Datum der Antragstellung
    contact_information = models.CharField(max_length=100)
    # bank_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT)
    description = models.TextField(max_length=4000)

    def __str__(self):
        return self.number


# class BankAccount(models.Model):
