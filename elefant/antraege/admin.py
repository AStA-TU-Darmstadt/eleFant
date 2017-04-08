from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Application)
admin.site.register(BankAccount)
admin.site.register(CarSharing)
admin.site.register(BudgetCategory)
