import Vue from 'vue'
import Router from 'vue-router'
import Signup from './views/Signup'
import Signout from './views/Signout'
import Login from './views/Login'
import Home from './views/Home'
import BankHome from './views/bank/BankHome'
import CustomerHome from './views/customer/CustomerHome'
import providerHome from './views/provider/providerHome'
import LoanTerm from './views/bank/LoanTerm'
import FundTerm from './views/bank/FundTerm'
import ListFundTerm from './views/provider/ListFundTerm'
import CreateNewFund from './views/provider/CreateNewFund'
import ListLoanTerm from './views/customer/ListLoanTerm'
import CreateNewLoan from './views/customer/CreateNewLoan'
import ListInstallments from './views/customer/ListInstallments'
import ListFundInstallments from './views/provider/ListFundInstallments'
import BankListFundInstallments from './views/bank/BankListFundInstallments'
import BankListFunds from './views/bank/BankListFunds'
import BankListLoans from './views/bank/BankListLoans'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup
    },
    {
      path: '/signout',
      name: 'signout',
      component: Signout
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/customer',
      name: 'customer',
      component: CustomerHome
    },
    {
      path: '/customer/new-loan',
      name: 'new-loan',
      component: ListLoanTerm
    },
    {
      path: '/customer/new-loan/:id',
      name: 'new-loan-creation',
      component: CreateNewLoan
    },
    {
      path: '/customer/installments/:id',
      name: 'installments',
      component: ListInstallments
    },
    {
      path: '/bank',
      name: 'bank',
      component: BankHome
    },
    {
      path: '/bank/loan-term',
      name: 'bank-loan-term',
      component: LoanTerm
    },
    {
      path: '/bank/pay-fund',
      name: 'bank-pay-fund',
      component: BankListFundInstallments
    },
    {
      path: '/bank/fund',
      name: 'bank-fund',
      component: BankListFunds
    },
    {
      path: '/bank/loan',
      name: 'bank-loan',
      component: BankListLoans
    },
    {
      path: '/bank/fund-term',
      name: 'bank-fund-term',
      component: FundTerm
    },
    {
      path: '/provider',
      name: 'provider',
      component: providerHome
    },
    {
      path: '/provider/new-fund',
      name: 'new-fund',
      component: ListFundTerm
    },
    {
      path: '/provider/new-fund/:id',
      name: 'new-fund-create',
      component: CreateNewFund
    },
    {
      path: '/provider/fund-installments/:id',
      name: 'fundinstallments',
      component: ListFundInstallments
    }
  ]
})
