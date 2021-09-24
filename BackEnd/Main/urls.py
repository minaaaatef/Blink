from django.conf.urls import url
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', csrf_exempt(views.UserCreate.as_view()), name='account-create'),
    path('login', views.loginApi.as_view(), name='account-login'),
    path('Attribute', views.AttributeRetrieve.as_view(), name='attribute'),

    ################# loan-fund-term ##############

    path('loan-fund-term', views.LoanFundTermView.as_view(), name='loan-fund-term'),
    path('loan-fund-term/<int:id>', views.LoanFundTermViewId.as_view(), name='loan-fund-term-id'),

    ################# loan-fund ##############

    path('loan-fund', views.LoanFundView.as_view(), name='loan-fund'),
    path('loan-fund/<int:id>', views.LoanFundViewId.as_view(), name='loan-fund-id'),

    ################# loan-term ##############

    path('loan-term', views.LoanTermView.as_view(), name='loan-term'),
    path('loan-term/<int:id>', views.LoanTermViewId.as_view(), name='loan-term-id'),

    ################# loan ##############

    path('loan', views.LoanView.as_view(), name='loan'),
    path('loan/<int:id>', views.LoanViewId.as_view(), name='loan-id'),
  
  
    path('pay-loan/<int:id>', views.PayLoan.as_view(), name='Pay-loan'),
    path('pay-fund/<int:id>', views.PayFund.as_view(), name='Pay-fund'),




    path('installments/<int:id>', views.InstallmentsView.as_view(), name='Installments-loan-id'),
    path('fund-installments/<int:id>', views.InstallmentsFundView.as_view(), name='Installments-loan-id'),
    path('fund-installments', views.BankInstallmentsFundView.as_view(), name='Installments-loan-id'),

    path('amortization', views.Amortization.as_view(), name='amortization'),

]
