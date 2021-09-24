<template>
  <v-container fluid>
    <Navbar :username=username />
    <ListObjects :url='LoanFundTermList.url' :attribute="LoanFundTermList.attribue" :actions="LoanFundTermList.actions" />
  </v-container>
</template>

<script>
import Navbar from '../../components/navbar'
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
          name: 'Create New',
          class: 'success',
          key: 'id',
          Function: function (id) {
            window.location.href = 'new-fund/' + id
          }
        }
      ]
    },
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
    Navbar
  }
}
</script>

<style></style>
