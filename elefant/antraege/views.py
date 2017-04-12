from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import generic

from .forms import *


class IndexView(generic.ListView):
    template_name = 'antraege/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Application.objects


def new_application(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create form instances #and populate them with data from the request:
        bank_account_form = BankAccountForm(request.POST)
        application_form = ApplicationForm(request.POST)

        # check whether the application is valid:
        if application_form.is_valid():
            # check if bank account already exists, if yes update it
            try:
                bank_account = BankAccount.objects.get(iban=request.POST['iban'])
                bank_account_form = BankAccountForm(request.POST, instance=bank_account)
            except ObjectDoesNotExist:
                pass
            bank_account = bank_account_form.save()

            # generate initial value for the application
            application = Application(application_date=timezone.now(), bank_account=bank_account)
            application.generate_application_number()

            application_form = ApplicationForm(request.POST, instance=application)
            application_form.save()
            return render(request, 'antraege/submitted_successfully.html',
                          {'application_form': application_form, 'bank_account_form': bank_account_form})
    else:
        # if a GET (or any other method) we'll create a blank form
        application_form = ApplicationForm()
        bank_account_form = BankAccountForm()
    return render(request, 'antraege/new_application.html',
                  {'application_form': application_form, 'bank_account_form': bank_account_form})


class ApplicationDetail(generic.DetailView):
    model = Application
    context_object_name = 'application'
    template_name = 'antraege/application_detail.html'
