import datetime

from rest_framework.response import Response
from rest_framework import status
from Main.serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from Main.models import *
import json
from rest_framework import generics
from amortization.schedule import amortization_schedule
from amortization.amount import calculate_amortization_amount
from dateutil.relativedelta import relativedelta
from .CalculationsFn import updateBankMoney
from .permissions import *
from rest_condition import Or


class UserCreate(generics.GenericAPIView):
    """
    Creates the user.
    """
    permission_classes = [AllowAny]
    http_method_names = ['post']
    serializer_class = UserSerializer

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                json['username'] = user.username
                json['userType'] = user.profile.Type
                json['userRoles'] = dict(user.profile.TYPE)
                return Response(json, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class loginApi(generics.GenericAPIView):
    """
    login the user.
    """
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        reqBody = json.loads(request.body)
        userName = reqBody['username']
        password = reqBody['password']
        try:
            user = User.objects.get(username=userName)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        if not check_password(password, user.password):
            raise ValidationError({"message": "Incorrect Login credentials"})

        if user:
            token, created = Token.objects.get_or_create(user=user)
            data = {}
            data['token'] = token.key
            data['username'] = user.username
            data['userType'] = user.profile.Type
            data['userRoles'] = user.profile.TYPE
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AttributeRetrieve(generics.GenericAPIView):
    """
    Get System Attributes
    """
    serializer_class = AttributeSerializers
    permission_classes = [BankPermissions]
    http_method_names = ['get']

    def get(self, request, format='json'):
        query = Attribute.get_solo()
        seriazer = AttributeSerializers(instance=query, many=False)
        return Response(seriazer.data, status=status.HTTP_200_OK)


#############################################################
####################### LoanFundTerm ########################
class LoanFundTermView(generics.GenericAPIView):
    """
    list and Create LoanFundTerm
    """
    serializer_class = LoanFundTermSerializers
    permission_classes = (Or(BankPermissions,ProviderPermissions),)
    queryset = LoanFundTerm.objects.all()

    def get(self, args):
        serializer = self.serializer_class(instance=LoanFundTerm.objects.all(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, args):
        self.request.data['bankPersonnel'] = self.request.user.id
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanFundTermViewId(generics.RetrieveUpdateDestroyAPIView):
    """
    Get LoanFundTerm instance
    """
    serializer_class = LoanFundTermSerializers
    permission_classes = (Or(BankPermissions,ProviderPermissions),)
    queryset = LoanFundTerm.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.canUpdateOrDelete:
            instance.bankPersonnel_id = self.request.user
            instance.Type = self.request.data['Type']
            instance.max = self.request.data['max']
            instance.min = self.request.data['min']
            instance.interestRate = self.request.data['interestRate']
            instance.duration = self.request.data['duration']
            instance.save()
            serializer = self.serializer_class(instance=instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data={'message': 'can not update instance'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.canUpdateOrDelete:
            self.perform_destroy(instance)
            return Response(data={'message': 'Deleted'},status=status.HTTP_200_OK)
        return Response(data={'message': 'can not delete instance'}, status=status.HTTP_400_BAD_REQUEST)


#############################################################
####################### LoanTerm ########################
class LoanTermView(generics.GenericAPIView):
    """
    list and Create LoanTerm
    """
    serializer_class = LoanTermSerializers
    permission_classes = (Or(BankPermissions,CustomerPermissions),)
    queryset = LoanTerm.objects.all()

    def get(self, args):
        serializer = self.serializer_class(instance=LoanTerm.objects.all(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, args):
        self.request.data['bankPersonnal'] = self.request.user.id
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanTermViewId(generics.RetrieveUpdateDestroyAPIView):
    """
    Get LoanTerm instance
    """
    serializer_class = LoanTermSerializers
    permission_classes = (Or(BankPermissions,CustomerPermissions),)
    queryset = LoanTerm.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.canUpdateOrDelete:
            instance.bankPersonnel_id = self.request.user
            instance.Type = self.request.data['Type']
            instance.max = self.request.data['max']
            instance.min = self.request.data['min']
            instance.interestRate = self.request.data['interestRate']
            if instance.isAvaliable:

                instance.isActive = True if 'isActive' in self.request.data and self.request.data[
                    'isActive'] == 'true' else False
            elif 'isActive' in self.request.data and instance.isActive != self.request.data['isActive']:
                return Response(data={'messages': 'can not activate instance, No availabe funds'},
                                status=status.HTTP_400_BAD_REQUEST)

            instance.save()

            serializer = self.serializer_class(instance=instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={'message': 'can not update instance'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.canUpdateOrDelete:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        return Response(data={'message': 'can not delete instance'}, status=status.HTTP_400_BAD_REQUEST)


#############################################################
####################### LoanFund ########################
class LoanFundView(generics.GenericAPIView):
    """
    list and Create Loan Fund
    """

    serializer_class = LoanFundSerializers
    permission_classes = (Or(BankPermissions,ProviderPermissions),)
    queryset = LoansFunds.objects.all()

    def get(self, args):
        if self.request.user.profile.Type == Profile.PROVIDERS:
            serializer = self.serializer_class(instance=LoansFunds.objects.filter(provider=self.request.user),
                                               many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        elif self.request.user.profile.Type == Profile.PERSONNEL:
            serializer = self.serializer_class(instance=LoansFunds.objects.all(),
                                               many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, args):
        self.request.data["provider"] = self.request.user.id
        self.request.data["bankPersonnal"] = None
        serializer = self.serializer_class(data=self.request.data)
        instance = LoansFunds()
        if serializer.is_valid():
            instance.loanFundTerm_id = self.request.data['loanFundTerm']
            instance.amount = self.request.data['amount']
            instance.startDate = self.request.data['startDate']
            instance.endDate = relativedelta(months=+instance.loanFundTerm.duration) + datetime.datetime.strptime( str(instance.startDate), '%Y-%m-%d').date()

            if self.request.user.profile.Type == Profile.PROVIDERS:
                instance.provider = self.request.user

            elif self.request.user.profile.Type == Profile.PERSONNEL:
                instance.bankPersonnal = self.request.user

            instance.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanFundViewId(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Loan Fund
    """
    serializer_class = LoanFundSerializers
    permission_classes = (Or(BankPermissions,ProviderPermissions),)
    queryset = LoansFunds.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        updateBankMoneyFlag = False


        if instance.canUpdateOrDelete:
            instance.loanFundTerm_id = self.request.data['loanFundTerm']
            instance.amount = self.request.data['amount']
            instance.startDate = self.request.data['startDate']

            # Make Sure the start date of the Loan Fund Is in the futere else set = Today
            if datetime.datetime.strptime( str(instance.startDate), '%Y-%m-%d').date()> datetime.date.today():
                instance.endDate = relativedelta(months=+instance.loanFundTerm.duration) + datetime.datetime.strptime( str(instance.startDate), '%Y-%m-%d').date()
            else:
                instance.startDate = datetime.date.today()
                instance.endDate = relativedelta(months=+instance.loanFundTerm.duration) + datetime.datetime.strptime( str(instance.startDate), '%Y-%m-%d').date()

            if self.request.user.profile.Type == Profile.CUSTOMERS:
                instance.provider_id = self.request.user

            elif self.request.user.profile.Type == Profile.PERSONNEL:
                instance.bankPersonnal_id = self.request.user
                if instance.isActive == False and 'isActive' in self.request.data and self.request.data[
                    'isActive'] == True :
                    instance.isActive = True
                    updateBankMoneyFlag = True
                    if instance.loanFundTerm.Type == LoanFundTerm.MONTHLY:
                        devider = 12
                    elif instance.loanFundTerm.Type == LoanFundTerm.YEARLY:
                        devider = 1
                    elif instance.loanFundTerm.Type == LoanFundTerm.QUARTERLY:
                        devider = 4
                    schedule = amortization_schedule(instance.amount,
                                                     instance.loanFundTerm.interestRate/devider,
                                                     instance.loanFundTerm.duration)

                    for number, amount, interest, principal, balance in schedule:
                        FundsInstallments.objects.create(amount=amount,
                                                         dueDate=datetime.datetime.strptime( str(instance.startDate), '%Y-%m-%d').date() + relativedelta(months=+number),
                                                         fund=instance
                                                         )

            instance.save()
            if updateBankMoneyFlag:
                if not updateBankMoney(instance.amount):
                    return Response(data={'message': 'No enough money'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(instance=instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={'message': 'can not update instance'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.canUpdateOrDelete:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        return Response(data={'message': 'can not delete instance'}, status=status.HTTP_400_BAD_REQUEST)


#############################################################
####################### Loan ########################
class LoanView(generics.GenericAPIView):
    """
    list and Create Loan Fund
    """

    serializer_class = LoanSerializers
    permission_classes = (Or(BankPermissions,CustomerPermissions),)
    queryset = LoansFunds.objects.all()

    def get(self, args):
        if self.request.user.profile.Type == Profile.CUSTOMERS:
            serializer = self.serializer_class(instance=Loan.objects.filter(customer=self.request.user),
                                               many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        elif self.request.user.profile.Type == Profile.PERSONNEL:
            serializer = self.serializer_class(instance=Loan.objects.all(),
                                               many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, args):
        self.request.data["customer"] = self.request.user.id
        self.request.data["bankPersonnal"] = None
        serializer = self.serializer_class(data=self.request.data)
        instance = Loan()
        if serializer.is_valid():
            instance.loanTerm_id = self.request.data['loanTerm']
            instance.amount = self.request.data['amount']
            instance.startDate = self.request.data['startDate']
            instance.endDate = relativedelta(months=+instance.loanTerm.duration) + datetime.datetime.strptime( instance.startDate, '%Y-%m-%d').date()

            if self.request.user.profile.Type == Profile.CUSTOMERS:
                instance.customer = self.request.user

            elif self.request.user.profile.Type == Profile.PERSONNEL:
                instance.bankPersonnal = self.request.user

            instance.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanViewId(generics.RetrieveUpdateDestroyAPIView):
    """
    Get LoanTerm Loan Fund
    """
    serializer_class = LoanSerializers
    permission_classes = (Or(BankPermissions,CustomerPermissions),)
    queryset = Loan.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        updateBankMoneyFlag = False

        if instance.canUpdateOrDelete:
            instance.loanTerm_id = self.request.data['loanTerm']
            instance.amount = self.request.data['amount']
            instance.startDate = self.request.data['startDate']
            instance.endDate = relativedelta(months=+instance.loanTerm.duration) + datetime.datetime.strptime( instance.startDate, '%Y-%m-%d').date()

            if self.request.user.profile.Type == Profile.CUSTOMERS:
                instance.provider_id = self.request.user

            elif self.request.user.profile.Type == Profile.PERSONNEL:
                instance.bankPersonnal_id = self.request.user
                # Make Sure the start date of the Loan Fund Is in the futere else set = Today

                if datetime.datetime.strptime( instance.startDate, '%Y-%m-%d').date() > datetime.date.today():
                    instance.endDate = relativedelta(months=+instance.loanTerm.duration) + datetime.datetime.strptime( instance.startDate, '%Y-%m-%d').date()
                else:
                    instance.startDate = datetime.date.today()
                    instance.endDate = relativedelta(months=+instance.loanTerm.duration) + instance.startDate

                if instance.isAvaliable:
                    if 'isActive' in self.request.data and self.request.data['isActive'] == True:
                        instance.isActive = True
                        updateBankMoneyFlag = True
                        if instance.loanTerm.Type == LoanFundTerm.MONTHLY:
                            devider = 12
                        elif instance.loanTerm.Type == LoanFundTerm.YEARLY:
                            devider = 1
                        elif instance.loanTerm.Type == LoanFundTerm.QUARTERLY:
                            devider = 4
                        schedule = amortization_schedule(instance.amount,
                                                         instance.loanTerm.activeInterestRate/devider,
                                                         instance.loanTerm.duration)

                        for number, amount, interest, principal, balance in schedule:
                            Installments.objects.create(amount=amount,
                                                        dueDate= datetime.datetime.strptime( str(instance.startDate), '%Y-%m-%d').date() + relativedelta(months=+number),
                                                        loan=instance
                                                        )
                else:
                    return Response(data={'message': 'can not Activate Instance, No Available funds'},
                                    status=status.HTTP_400_BAD_REQUEST)

            instance.save()
            if updateBankMoneyFlag:
                if not updateBankMoney(-instance.amount):
                    return Response(data={'message': 'No enough money'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(instance=instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={'message': 'can not update instance'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.canUpdateOrDelete:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        return Response(data={'message': 'can not delete instance'}, status=status.HTTP_400_BAD_REQUEST)


class Amortization(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = AmortizationInputSerizlizer

    def post(self, request, *args, **kwargs):

        self.serializer_class = AmortizationInputSerizlizer
        serializer = AttributeSerializers(data=request.data)
        if serializer.is_valid():

            finalAmount = calculate_amortization_amount(int(self.request.data['amount']),
                                                        self.request.data['interest']/12,
                                                        self.request.data['duration'])

            schedule = amortization_schedule(int(self.request.data['amount']),
                                             self.request.data['interest']/12,
                                             self.request.data['duration'])

            scheduleDict = {}
            scheduleDict['schedule'] = {}
            scheduleDict['finalAmount'] = finalAmount

            for number, amount, interest, principal, balance in schedule:
                scheduleDict['schedule'][number] = {'amount': amount,
                                                    'number':number,
                                                    'interest': interest,
                                                    'principal': principal,
                                                    'balance': balance,
                                                    }
            return Response(data=scheduleDict, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayLoan(generics.GenericAPIView):
    serializer_class = InstallmentsSerializers
    permission_classes = [CustomerPermissions]
    queryset = Installments.objects.all()
    lookup_field = 'id'
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.loan.customer == self.request.user:
            instance.paid = True
            instance.save()
            if not updateBankMoney(instance.amount):
                return Response(data={'message': 'No enough money'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_200_OK)




class PayFund(generics.GenericAPIView):
    serializer_class = FundsInstallmentsSerializers
    permission_classes = [BankPermissions]
    queryset = FundsInstallments.objects.all()
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        attribute = Attribute.get_solo()
        if instance.canPay:
            instance.paid = True
            instance.save()
            if not updateBankMoney(-instance.amount):
                return Response(data={'message': 'No enough money'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(data={'message':'Not enough money can not pay' }, status=status.HTTP_400_BAD_REQUEST)




class InstallmentsFundView(generics.GenericAPIView):
    serializer_class = FundsInstallmentsSerializers
    permission_classes = (Or(BankPermissions,ProviderPermissions),)
    queryset = FundsInstallments.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if self.request.user.profile.Type == Profile.PROVIDERS:
            instance = FundsInstallments.objects.filter(fund=kwargs['id'],paid=False)
            serializer = FundsInstallmentsSerializers(instance=instance,many=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)



class BankInstallmentsFundView(generics.GenericAPIView):
    serializer_class = FundsInstallmentsSerializers
    permission_classes = (Or(BankPermissions,ProviderPermissions),)
    queryset = FundsInstallments.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if self.request.user.profile.Type == Profile.PERSONNEL:
            instance = FundsInstallments.objects.filter(paid=False).order_by('dueDate')
            serializer = FundsInstallmentsSerializers(instance=instance, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class InstallmentsView(generics.GenericAPIView):
    serializer_class = InstallmentsSerializers
    permission_classes = (Or(BankPermissions,CustomerPermissions),)
    queryset = Installments.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if self.request.user.profile.Type == Profile.CUSTOMERS:
            instance = Installments.objects.filter(loan_id=kwargs['id'],paid=False)
            serializer = InstallmentsSerializers(instance=instance,many=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)