# Create your models here.
from  .models import *
from django.db import transaction

@transaction.atomic
def updateBankMoney(value):
    attribute = Attribute.get_solo()
    attribute.bankAccountMoney += value
    if attribute.bankAccountMoney > 0:
        attribute.save()
        return True
    else:
        return False