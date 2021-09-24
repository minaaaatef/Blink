from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=6, max_length=100,
                                     write_only=True)

    type = serializers.IntegerField(
        required=True,
        source="profile.Type"
    )

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        user.profile.Type = validated_data['profile']['Type']
        user.profile.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'type')


class AttributeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class LoanFundTermSerializers(serializers.ModelSerializer):
    canUpdateOrDelete = serializers.SerializerMethodField()

    def get_canUpdateOrDelete(self, instance):
        if isinstance(instance, LoanFundTerm):
            return instance.canUpdateOrDelete
        else:
            return None

    class Meta:
        model = LoanFundTerm
        fields = '__all__'


class LoanFundSerializers(serializers.ModelSerializer):
    canUpdateOrDelete = serializers.SerializerMethodField()
    loanFundTermObject = serializers.SerializerMethodField()

    def get_loanFundTermObject(self, instance):
        if isinstance(instance, LoansFunds):
            return LoanFundTermSerializers(instance=instance.loanFundTerm).data
        else:
            return None
    def get_canUpdateOrDelete(self, instance):
        if isinstance(instance, LoansFunds):
            return instance.canUpdateOrDelete
        else:
            return None

    class Meta:
        model = LoansFunds
        fields = '__all__'


class LoanTermSerializers(serializers.ModelSerializer):
    isAvaliable = serializers.SerializerMethodField()
    canUpdateOrDelete = serializers.SerializerMethodField()
    activeInterestRate = serializers.SerializerMethodField()

    def get_activeInterestRate(self, instance):
        if isinstance(instance, LoanTerm):
            return instance.activeInterestRate
        else:
            return None

    def get_isAvaliable(self, instance):
        if isinstance(instance, LoanTerm):
            return instance.isAvaliable
        else:
            return None

    def get_canUpdateOrDelete(self, instance):
        if isinstance(instance, LoanTerm):
            return instance.canUpdateOrDelete
        else:
            return None

    class Meta:
        model = LoanTerm
        fields = '__all__'


class LoanSerializers(serializers.ModelSerializer):
    isAvaliable = serializers.SerializerMethodField()
    canUpdateOrDelete = serializers.SerializerMethodField()
    loanTermObject = serializers.SerializerMethodField()

    def get_loanTermObject(self, instance):
        if isinstance(instance, Loan):
            return LoanTermSerializers(instance=instance.loanTerm).data
        else:
            return None

    def get_isAvaliable(self, instance):
        if isinstance(instance, Loan):
            return instance.isAvaliable
        else:
            return None

    def get_canUpdateOrDelete(self, instance):
        if isinstance(instance, Loan):
            return instance.canUpdateOrDelete
        else:
            return None

    class Meta:
        model = Loan
        fields = '__all__'

class AmortizationInputSerizlizer(serializers.Serializer):
    amount = serializers.IntegerField()
    interest = serializers.FloatField()
    duration = serializers.IntegerField()


class InstallmentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Installments
        fields = '__all__'


class FundsInstallmentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = FundsInstallments
        fields = '__all__'
