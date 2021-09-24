from django.contrib import admin
from .models import *
from django.contrib import admin
from solo.admin import SingletonModelAdmin

# Register your models here.

admin.site.register(Profile)
admin.site.register(LoanFundTerm)
admin.site.register(LoansFunds)
admin.site.register(LoanTerm)
admin.site.register(Loan)

admin.site.register(Attribute, SingletonModelAdmin)
