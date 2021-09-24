<template>
  <v-container fluid>
    <Navbar :username=username />

  </v-container>
</template>

<script>
import Navbar from '../components/navbar.vue'

export default {
  data: () => ({
    username: '',
    token: '',
    type: '',
    Providers: 1,
    Customers: 2,
    Personnel: 3,
    roles: {
      Providers: 'Loan Providers',
      Customers: 'Loan Customers',
      Personnel: 'Bank Personnel'
    }
  }),
  beforeMount() {
    const myStorage = window.localStorage
    this.token = myStorage.getItem('token')
    this.username = myStorage.getItem('username')
    this.type = parseInt(myStorage.getItem('userType'))
    if (this.type === this.Providers) {
      window.location.href = 'provider'
    }
    if (this.type === this.Personnel) {
      window.location.href = 'bank'
    }
    if (this.type === this.Customers) {
      window.location.href = 'customer'
    }
  },
  components: {
    Navbar
  }
}
</script>

<style></style>
