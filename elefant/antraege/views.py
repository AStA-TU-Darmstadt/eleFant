from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
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
            bank_account = bank_account_form.save()  # this validates the form

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
    return render(request, 'antraege/application_form.html',
                  {'application_form': application_form, 'bank_account_form': bank_account_form})


def search_application(request):
    if request.method == 'POST':
        try:
            reference_number = UUID(request.POST['reference_number'])  # check if ref_nr is a valid uuid
            if Application.objects.filter(pk=reference_number).exists():  # check if application with this ref_nr exists
                return HttpResponseRedirect(reverse('antraege:detail', args=(reference_number,)))
        except ValueError:
            pass
    return render(request, 'antraege/search_application.html')


class ApplicationCreate(generic.CreateView):
    model = Application
    fields = ['applicant', 'contact', 'e_mail', 'description', 'total_amount']

    # generate empty bank account form
    bank_account_form = BankAccountForm()

    def get_context_data(self, **kwargs):
        # add bank account form to the context to make it usable in the template
        context = super(ApplicationCreate, self).get_context_data(**kwargs)
        context['bank_account_form'] = self.bank_account_form

        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        # process bank_account form
        try:
            # check if this bank account is already in the system
            bank_account = BankAccount.objects.get(iban=request.POST['iban'])
            self.bank_account_form = BankAccountForm(request.POST, instance=bank_account)
        except ObjectDoesNotExist:
            self.bank_account_form = BankAccountForm(self.request.POST)

        if self.bank_account_form.is_valid():
            # proceed with standard implementation
            return super(ApplicationCreate, self).post(self, request, *args, **kwargs)
        else:
            return super(ApplicationCreate, self).form_invalid(self.get_form())

    def form_valid(self, form):
        # save bank account
        bank_account = self.bank_account_form.save()

        # generate initial values for the new application
        # noinspection PyAttributeOutsideInit
        self.object = Application(application_date=timezone.now(), bank_account=bank_account)
        self.object.generate_application_number()
        form = self.get_form()
        form.instance = self.object

        return super(ApplicationCreate, self).form_valid(form)


class ApplicationDetail(generic.DetailView):
    model = Application
    context_object_name = 'application'


class ApplicationEdit(generic.UpdateView):
    template_name = 'antraege/application_form.html'
    model = Application
    form_class = ApplicationForm

    def get_context_data(self, **kwargs):
        # add application_number to context as headline
        context = super(ApplicationEdit, self).get_context_data(**kwargs)
        application_number = get_object_or_404(Application, pk=self.kwargs.get('pk')).application_number
        context['headline'] = application_number
        return context
