# Create your models here.
from  .models import *
from django.db import transaction

@transaction.atomic
def updateBankMoney(value):
    attribute = Attribute.get_solo()
    attribute.bankAccountMoney += value
    attribute.save()
    pass
