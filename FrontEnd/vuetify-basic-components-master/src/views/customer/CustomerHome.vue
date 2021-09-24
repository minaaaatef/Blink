<template>
  <v-container fluid>
    <Navbar :username=username />
    <v-btn class="ma-2" @click="goTo('new-loan')"> View Loan Terms </v-btn>
    <v-spacer></v-spacer>

    <ListObjects :url='LoanList.url' :attribute="LoanList.attribue" :actions="LoanList.actions" />
  </v-container>
</template>

<script>
import Navbar from '../../components/navbar'
import ListObjects from '../../components/ListObjects'

export default {
  data: () => ({

    LoanList: {
      url: 'http://127.0.0.1:8000/loan',
      attribue: [
        { name: 'amount', type: 'text', data: '' },
        { name: 'endDate', type: 'text', data: '' },
        { name: 'startDate', type: 'text', data: '' },
        { name: 'isActive', type: 'text', data: '' }
      ],
      actions: [
        {
          name: 'delete',
          class: 'error',
          key: 'id',
          ifTruecondition: true,
          ifFalsecondition: 'isActive',
          Function: function (id) {
            this.token = window.localStorage.getItem('token')
            const requestOptions = {
              method: 'DELETE',
              headers: { Authorization: 'Token ' + this.token, 'Content-Type': 'application/json' }
            }
            fetch('http://127.0.0.1:8000/loan/' + id, requestOptions)
              .then(response => {
                // window.location.reload()
              })
              .catch(function (error) {
                console.log(error)
              })
          }
        },
        {
          name: 'Show installments',
          class: 'success ml-2',
          key: 'id',
          ifTruecondition: 'isActive',
          ifFalsecondition: 'id',
          Function: function (id) {
            window.location.href = window.location.href + '/installments/' + id
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
  },
  methods: {
    goTo (name) {
      this.$router.push({ name: name })
    }
  }
}
</script>

<style></style>
