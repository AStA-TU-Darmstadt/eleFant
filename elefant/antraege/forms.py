from django.forms import ModelForm


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['applicant', 'contact', 'contact_information', 'description', 'total_amount']


class BankAccountForm(ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_holder', 'iban', 'bic', 'bank']


class CarSharingForm(ModelForm):
    class Meta:
        model = CarSharing
        fields = ['kilometres', 'rental_duration']
