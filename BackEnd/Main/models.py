from turtle import mode

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from solo.models import SingletonModel




class Profile(models.Model):
    PROVIDERS = 1
    CUSTOMERS = 2
    PERSONNEL = 3

    TYPE = (
        (PROVIDERS, 'Loan Providers'),
        (CUSTOMERS, 'Loan Customers'),
        (PERSONNEL, 'Bank Personnel'),
    )

    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    Type = models.IntegerField(choices=TYPE, default=CUSTOMERS)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class LoansFunds(models.Model):
    provider = models.ForeignKey(User, on_delete=models.PROTECT)
    bankPersonnal = models.ForeignKey(User, on_delete=models.PROTECT, related_name='loanFunds', null=True, blank=True)
    loanFundTerm = models.ForeignKey('LoanFundTerm', on_delete=models.PROTECT, related_name='loanFunds')
    amount = models.IntegerField()
    startDate = models.DateField()
    endDate = models.DateField(blank=True,null=True)
    isActive = models.BooleanField(default=False)

    @property
    def canUpdateOrDelete(self):
        return not self.isActive


class LoanFundTerm(models.Model):
    YEARLY = 1
    MONTHLY = 2
    QUARTERLY = 3

    TYPE = (
        (YEARLY, 'Yearly'),
        (MONTHLY, 'Monthly'),
        (QUARTERLY, 'Quarterly'),
    )

    bankPersonnel = models.ForeignKey(User, on_delete=models.PROTECT, related_name='LoanFundTerm')
    Type = models.IntegerField(choices=TYPE, default=MONTHLY)
    max = models.IntegerField()
    min = models.IntegerField()
    interestRate = models.FloatField(null=False, blank=False)
    duration = models.IntegerField(default=12)

    @property
    def canUpdateOrDelete(self):
        return not self.loanFunds.exists()


class LoanTerm(models.Model):
    YEARLY = 1
    MONTHLY = 2
    QUARTERLY = 3

    TYPE = (
        (YEARLY, 'Yearly'),
        (MONTHLY, 'Monthly'),
        (QUARTERLY, 'Quarterly'),
    )

    bankPersonnal = models.ForeignKey(User, on_delete=models.PROTECT, related_name='LoanTerm')
    Type = models.IntegerField(choices=TYPE, default=MONTHLY)
    interestRate = models.FloatField(null=False, blank=False)
    max = models.IntegerField()
    min = models.IntegerField()
    BankProfitRate = models.FloatField(default=0.01)
    RiskRate = models.FloatField(default=0.02)
    duration = models.IntegerField(default=12)

    @property
    def activeInterestRate(self):
        return self.BankProfitRate + self.RiskRate + self.interestRate

    @property
    def isAvaliable(self):
        attribute = Attribute.get_solo()
        return int(self.max) < int(attribute.bankAccountMoney)

    @property
    def canUpdateOrDelete(self):
        return not self.loans.exists()


class Loan(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='loans')
    bankPersonnel = models.ForeignKey(User, on_delete=models.PROTECT, related_name='loansApproved',null=True,blank=True)
    loanTerm = models.ForeignKey('LoanTerm', on_delete=models.PROTECT, related_name='loans')
    amount = models.IntegerField()
    startDate = models.DateField()
    endDate = models.DateField(null=True,blank=True)
    isActive = models.BooleanField(default=False)

    @property
    def isAvaliable(self):
        attribute = Attribute.get_solo()
        return self.amount < attribute.bankAccountMoney

    @property
    def canUpdateOrDelete(self):
        return not self.isActive


class Installments(models.Model):
    dueDate = models.DateField(null=False, blank=False)
    loan = models.ForeignKey('Loan', related_name='installments', on_delete=models.CASCADE)
    amount = models.FloatField(null=False, blank=False)
    paid = models.BooleanField(default=False)


class FundsInstallments(models.Model):
    dueDate = models.DateField(null=False, blank=False)
    fund = models.ForeignKey('LoansFunds', related_name='installments', on_delete=models.CASCADE)
    amount = models.FloatField(null=False, blank=False)
    paid = models.BooleanField(default=False)


class Attribute(SingletonModel):
    interestRate = models.FloatField(default=0.07)
    BankProfitRate = models.FloatField(default=0.01)
    RiskRate = models.FloatField(default=0.02)
    bankAccountMoney = models.FloatField(default=100000)
    maxAcceptedLoanFund = models.IntegerField(default=500000)
    maxAcceptedLoan = models.IntegerField(default=100000)
