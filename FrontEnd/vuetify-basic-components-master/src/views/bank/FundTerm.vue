<template>
  <v-container fluid>
    <Navbar :username=username typeRole="bank" />
    <v-btn class="mt-4 info" @click="showCreationFundTerm = !showCreationFundTerm">Create New Fund Term</v-btn>
    <v-spacer></v-spacer>
    <CreateFundTerm v-if="showCreationFundTerm" />
        <h1>Fund Term</h1>
    <ListObjects :url='LoanFundTermList.url' :attribute="LoanFundTermList.attribue" :actions="LoanFundTermList.actions" />
     </v-container>
</template>
<script>
import Navbar from '../../components/navbar'
import CreateFundTerm from './CreateFundTerm'
import ListObjects from '../../components/ListObjects'

export default {
  data: () => ({

    LoanFundTermList: {
      url: 'http://127.0.0.1:8000/loan-fund-term',
      attribue: [
        { name: 'Type', type: 'select', data: { 1: 'Yearly', 2: 'Monthly', 3: 'Quarterly' } },
        { name: 'max', type: 'text', data: '' },
        { name: 'min', type: 'text', data: '' },
        { name: 'interestRate', type: 'percentage', data: '' }
      ],
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
            fetch('http://127.0.0.1:8000/loan-fund-term/' + id, requestOptions)
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
    showCreationFundTerm: false,
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
    CreateFundTerm
  }
}
</script>

<style></style>
