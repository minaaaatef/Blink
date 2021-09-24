<template>
  <v-container fluid>
    <Navbar :username=username typeRole="bank" />
    <ListObjects  :url='InstallmentsList.url' :attribute="InstallmentsList.attribue" :actions="InstallmentsList.actions" />
  </v-container>
</template>

<script>
import Navbar from '../../components/navbar'
import ListObjects from '../../components/ListObjects'

export default {
  data: () => ({
    InstallmentsList: {
      url: 'http://127.0.0.1:8000/fund-installments',
      attribue: [
        { name: 'amount', type: 'number', data: '' },
        { name: 'dueDate', type: 'text', data: '' }
      ],
      actions: [
        {
          name: 'Pay Fund Installments',
          class: 'success',
          key: 'id',
          Function: function (id) {
            this.token = window.localStorage.getItem('token')
            const requestOptions = {
              method: 'POST',
              headers: { Authorization: 'Token ' + this.token, 'Content-Type': 'application/json' }
            }
            fetch('http://127.0.0.1:8000/pay-fund/' + id, requestOptions)
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
