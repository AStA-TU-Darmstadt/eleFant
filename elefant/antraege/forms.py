from django.forms import ModelForm

from .models import *


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['applicant', 'contact', 'e_mail', 'description', 'total_amount']
        localized_fields = '__all__'


class ApplicationFormAll(ModelForm):
    class Meta:
        model = Application
        exclude = ['application_date']
        localized_fields = '__all__'


class BankAccountForm(ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_holder', 'iban', 'bic', 'bank']


class CarSharingForm(ModelForm):
    class Meta:
        model = CarSharing
        fields = ['kilometres', 'rental_duration']
