from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class Application(models.Model):  # Finanzantrag
    application_number = models.CharField(primary_key=True, max_length=20)  # FA-Nummer
    application_date = models.DateTimeField('date of application')  # Datum der Antragstellung

    applicant = models.CharField(max_length=70)  # Antragsteller*in
    contact = models.CharField(max_length=70)  # Ansprechpartner*in
    contact_information = models.CharField(max_length=100)

    bank_account = models.ForeignKey('BankAccount', on_delete=models.PROTECT)

    description = models.TextField(max_length=4000)  # Verwendungszweck

    carsharing_data = models.ForeignKey('CarSharing')  # car sharing

    total_amount = models.DecimalField(max_digits=11, decimal_places=2)  # allow applications up to 999 999 999.99€

    APPLIED = 'APP'
    QUERIES = 'QUE'
    APPROVED = 'APV'
    DECLINED = 'DCL'
    STATUS_CHOICES = (
        (APPLIED, 'applied'),  # beantragt
        (QUERIES, 'queries'),  # Rückfragen
        (APPROVED, 'approved'),  # genehmigt
        (DECLINED, 'declined'),  # abgelehnt
    )

    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=APPLIED,
    )

    approval_date = models.DateTimeField('date of approval', blank=True)  # genehmigt am
    approval_place = models.CharField('place of approval', max_length=70)  # genehmigt auf

    budget_category = models.ForeignKey('BudgetCategory', on_delete=models.PROTECT)  # Haushaltstopf

    def __str__(self):
        return self.application_number

    def clean(self):
        # Don't allow unapproved entries to have an approval_date
        if self.status != self.APPROVED and self.approval_date is not None:
            raise ValidationError({'approval_date': _('Applications without approval may not hav an approval date.')})


class BankAccount(models.Model):
    account_holder = models.CharField(max_length=70)
    iban = models.CharField(primary_key=True, max_length=34)
    bank = models.CharField(max_length=50)
    bic = models.CharField(max_length=11)


class CarSharing(models.Model):
    rental_duration = models.TimeField()  # Leihdauer
    kilometres = models.PositiveSmallIntegerField()  # Kilometeranzahl


class BudgetCategory(models.Model):
    name = models.CharField(primary_key=True, max_length=70)
    category_budget_total = models.DecimalField(max_digits=11, decimal_places=2)  # allow budgets up to 999 999 999.99€

    def budget_left(self):
        """Returns how much budget is left for this budget category."""
        return self.category_budget_total - self.application_set.aggregate(Sum('total_amount'))
