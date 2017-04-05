from django.test import TestCase
from django.utils import timezone
from antraege.models import *


def create_application(applicant, application_number, contact_information, bank_account, description,
                       total_amount, budget_category, contact='', carsharing_data=None, approval_date=None,
                       approved_by='', status=Application.APPLIED):
    time = timezone.now()

    return Application.objects.create(application_number=application_number
                                      , application_date=time, applicant=applicant,
                                      contact=contact, contact_information=contact_information,
                                      bank_account=bank_account,
                                      description=description, carsharing_data=carsharing_data,
                                      total_amount=total_amount,
                                      status=status, budget_category=budget_category, approval_date=approval_date,
                                      approved_by=approved_by)


def create_bank_account(account_holder, iban, bank, bic):
    return BankAccount.objects.create(account_holder=account_holder, iban=iban, bank=bank, bic=bic)


def create_budget_category(name, category_budget_total):
    return BudgetCategory.objects.create(name=name, category_budget_total=category_budget_total)


class ApplicationModelTests(TestCase):
    def setUp(self):
        create_bank_account(account_holder='Max Mustermann', iban='DE12500105170648489890', bank='Musterbank Darmstadt',
                            bic='12')
        bank_account = BankAccount.objects.get(iban='DE12500105170648489890')

        create_budget_category(name='Fachschaften', category_budget_total=100)
        category = BudgetCategory.objects.get(name='Fachschaften')

        create_application(application_number='1', applicant='Max Mustermann', contact_information='test@example.com',
                           bank_account=bank_account, description="This is a test application.", total_amount=1000.50,
                           budget_category=category)

    def test_status_is_applied(self):
        application = Application.objects.get(application_number='1')
        self.assertEqual(application.status, Application.APPLIED)

    def test_approval_date_without_approved(self):
        application = Application.objects.get(application_number='1')
        application.approval_date = timezone.now()
        application.save()
        self.assertEqual(application.status, Application.APPLIED)
        with self.assertRaises(ValidationError):
            application.clean()

    def test_approved_without_approval_date_and_by(self):
        application = Application.objects.get(application_number='1')
        application.status = Application.APPROVED
        application.save()
        with self.assertRaises(ValidationError):
            application.clean()

    def test_approved_without_approved_by(self):
        application = Application.objects.get(application_number='1')
        application.status = Application.APPROVED
        application.approval_date = timezone.now()
        application.save()
        with self.assertRaises(ValidationError):
            application.clean()