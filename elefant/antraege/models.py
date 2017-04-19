import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Application(models.Model):  # Finanzantrag
    application_number = models.CharField(db_index=True, max_length=20)  # FA-Nummer
    application_date = models.DateTimeField('date of application')  # Datum der Antragstellung
    reference_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Referenznummer

    applicant = models.CharField(max_length=70)  # Antragsteller*in
    contact = models.CharField(max_length=70, blank=True)  # Ansprechpartner*in
    e_mail = models.EmailField()  # E-Mail

    bank_account = models.ForeignKey('BankAccount', on_delete=models.PROTECT)

    description = models.TextField(max_length=4000)  # Verwendungszweck

    carsharing_data = models.ForeignKey('CarSharing', blank=True, null=True)  # car sharing

    total_amount = models.DecimalField(max_digits=11, decimal_places=2)  # allow applications up to 999 999 999.99euro

    APPLIED = 'APP'
    QUERIES = 'QUE'
    APPROVED = 'APV'
    DECLINED = 'DCL'
    STATUS_CHOICES = (
        (APPLIED, 'applied'),  # beantragt
        (QUERIES, 'queries'),  # Rueckfragen
        (APPROVED, 'approved'),  # genehmigt
        (DECLINED, 'declined'),  # abgelehnt
    )

    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=APPLIED,
    )

    approval_date = models.DateTimeField('date of approval', blank=True, null=True)  # genehmigt am
    approved_by = models.CharField(max_length=70, blank=True)  # genehmigt auf

    budget_category = models.ForeignKey('BudgetCategory', on_delete=models.PROTECT, blank=True,
                                        null=True)  # Haushaltstopf

    def __str__(self):
        return self.application_number

    def clean(self):
        # Don't allow unapproved entries to have an approval_date or approved_by
        if self.status != self.APPROVED and (self.approval_date is not None or self.approved_by != ''):
            raise ValidationError(
                {'approval_date': _('Applications without approval may not have an approval date or place.')})
        # Don't allow approved entries without approval_date or approved_by
        if self.status == self.APPROVED and (self.approval_date is None or self.approved_by == ''):
            raise ValidationError({'status': _('Approved Applications must have an approval date and place.')})

    def generate_application_number(self, number=None):
        """Generates the application number for new applications. Should only be called once upon creation."""
        # get year
        year = str(timezone.now().year)[-2:]
        # get next number
        if number is None:
            if Application.objects.count() > 0:
                number = int(Application.objects.order_by('application_date').reverse()[0].application_number[5:]) + 1
            else:
                number = 1
        self.application_number = 'FA' + year + '-' + str(number)


class BankAccount(models.Model):
    account_holder = models.CharField(max_length=70)
    iban = models.CharField(primary_key=True, max_length=34)
    bank = models.CharField(max_length=50)
    bic = models.CharField(max_length=11)

    def __str__(self):
        return self.iban


class CarSharing(models.Model):
    rental_duration = models.TimeField()  # Leihdauer
    kilometres = models.PositiveSmallIntegerField()  # Kilometeranzahl


class BudgetCategory(models.Model):
    name = models.CharField(primary_key=True, max_length=70)
    category_budget_total = models.DecimalField(max_digits=11, decimal_places=2)  # allow budgets up to 999 999 999.99euro

    def __str__(self):
        return self.name

    def budget_left(self):
        """Returns how much budget is left for this budget category."""
        return self.category_budget_total - self.application_set.aggregate(Sum('total_amount'))
