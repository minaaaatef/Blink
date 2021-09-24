<template>
  <v-container fluid>
    <Navbar :username=username typeRole="bank" />
    <v-spacer></v-spacer>
    <v-btn class="mt-4 info" @click="showCreationLoanTerm = !showCreationLoanTerm">Create New Loan Term</v-btn>
    <CreateLoanTerm v-if="showCreationLoanTerm" />
    <h1>Loan Term</h1>
    <ListObjects :key="updateLoanTermList" :url='LoanTermList.url' :attribute="LoanTermList.attribue" :actions="LoanTermList.actions" />
  </v-container>
</template>
<script>
import Navbar from '../../components/navbar'
import CreateLoanTerm from './CreateLoanTerm'
import ListObjects from '../../components/ListObjects'

export default {
  data: () => ({

    LoanTermList: {
      url: 'http://127.0.0.1:8000/loan-term',
      attribue: [
        { name: 'max', type: 'text', data: '' },
        { name: 'min', type: 'text', data: '' },
        { name: 'interestRate', type: 'percentage', data: '' },
        { name: 'BankProfitRate', type: 'text', data: '' }
      ],
      update: 0,
      actions: [
        {
          name: 'delete',
          class: 'error',
          key: 'id',
          Function: function (id) {
            this.token = window.localStorage.getItem('token')
            const requestOptions = {
              method: 'DELETE',
              headers: { Authorization: 'Token ' + this.token, 'Content-Type': 'application/json' }
            }
            fetch('http://127.0.0.1:8000/loan-term/' + id, requestOptions)
              .then(response => {
                window.location.reload()
              })
              .catch(function (error) {
                console.log(error)
              })
          }
        }

      ]
    },
    showCreationLoanTerm: false,
    username: '',
    token: '',
    roles: '',
    Providers: 1,
    Customers: 2,
    Personnel: 3,
    type: {
      Providers: 'Loan Providers',
      Customers: 'Loan Customers',
      Personnel: 'Bank Personnel'
    }
  }),

  beforeMount() {
    const myStorage = window.localStorage
    this.token = myStorage.getItem('token')
    this.username = myStorage.getItem('username')
    this.roles = myStorage.getItem('userType')
    this.type = myStorage.getItem('userRoles')
    console.log(this.token)
    console.log(this.username)
    console.log(this.roles)
    console.log(this.type)
  },
  components: {
    ListObjects,
    Navbar,
    CreateLoanTerm
  }
}
</script>

<style></style>
