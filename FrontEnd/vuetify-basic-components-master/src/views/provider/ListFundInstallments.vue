<template>
  <v-container fluid>
    <Navbar :username=username />
    <ListObjects  :url='InstallmentsList.url' :attribute="InstallmentsList.attribue" :actions="InstallmentsList.actions" />
  </v-container>
</template>

<script>
import Navbar from '../../components/navbar'
import ListObjects from '../../components/ListObjects'

export default {
  data: () => ({
    InstallmentsList: {
      url: 'http://127.0.0.1:8000/fund-installments/',
      attribue: [
        { name: 'amount', type: 'number', data: '' },
        { name: 'dueDate', type: 'text', data: '' }
      ],
      actions: [
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
    console.log()
    this.InstallmentsList.url = this.InstallmentsList.url + this.$route.params.id

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
