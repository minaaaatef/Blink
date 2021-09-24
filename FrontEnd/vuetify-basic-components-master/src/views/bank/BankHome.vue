<template>
  <v-container fluid>
    <Navbar :username=username typeRole="bank" />
    <v-btn class="ma-2" @click="goTo('bank-fund-term')"> loan Fund Term</v-btn>
    <v-spacer></v-spacer>
    <v-btn class="ma-2" @click="goTo('bank-fund')"> loan Funds </v-btn>
    <v-spacer></v-spacer>
    <v-btn class="ma-2" @click="goTo('bank-loan')"> loans </v-btn>
    <v-spacer></v-spacer>
    <v-btn class="ma-2" @click="goTo('bank-loan-term')"> loan Term</v-btn>
    <v-spacer></v-spacer>
    <v-btn class="ma-2" @click="goTo('bank-pay-fund')"> Pay Fund</v-btn>
    <v-spacer></v-spacer>
  </v-container>
</template>
<script>
import Navbar from '../../components/navbar'

export default {
  data: () => ({
    username: '',
    token: '',
    roles: '',
    Attribute: '',
    Providers: 1,
    Customers: 2,
    Personnel: 3,
    type: {
      Providers: 'Loan Providers',
      Customers: 'Loan Customers',
      Personnel: 'Bank Personnel'
    }
  }),
  mounted() {
    this.token = window.localStorage.getItem('token')

    const requestOptions = {
      method: 'GET',
      headers: { Authorization: 'Token ' + this.token }
    }

    fetch('http://127.0.0.1:8000/Attribute', requestOptions)
      .then(response => {
        response.json().then(data => {
          console.log(data)
          this.Attribute = data
        })
      })
      .catch(function (error) {
        console.log(error)
      })
  },

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
