<template>
  <v-container fluid>
    <Navbar :username=username />
    <v-card>
      <v-card-title>
        create New Fund
      </v-card-title>
      <v-card-text>

        <h1>you are applying for a fund</h1>

         <h2 class="mt-5"> Interest Rate: {{Data.interestRate}} </h2>
         <h2 class="mt-5"> Duration: {{Data.duration}} Months  </h2>
         <h2 class="mt-5"> Please Enter The Starting Date and The Amount  </h2>
        <v-form>
           <v-text-field
          v-model="startDate"
          label="starting date"
          required
          type="date"
          :rules="retrunDateRules()"
        ></v-text-field>
         <h2 class="mt-5"> Please note that The Max is {{Data.max}} and the Min is {{Data.min}}  </h2>

          <v-text-field
          v-model="amount"
          label="Amount"
          required
          type="number"
          :rules="retrunDateRules()"
        ></v-text-field>
          <Amortization url="http://127.0.0.1:8000/amortization" :amount="amount" :duration="Data.duration" :interestRate="Data.interestRate" :key="amount" />
        <v-btn class="success" @click="submit">Submit</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import Navbar from '../../components/navbar'
import Amortization from '../../components/Amortization'

export default {
  data: () => ({
    amount: '',
    startDate: '',
    Data: '',
    url: 'http://127.0.0.1:8000/loan-fund-term/',
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
    const requestOptions = {
      method: 'GET',
      headers: { Authorization: 'Token ' + this.token, 'Content-Type': 'application/json' }
    }

    fetch(this.url + this.$route.params.id, requestOptions)
      .then(response => {
        response.json().then(data => {
          console.log(data)
          this.Data = data
        })
      }).catch(function (error) {
        console.log(error)
      })
  },
  methods: {
    retrunAmountRules() {
      return [
        v => !!v || 'This field is required',
        v => (v && v >= this.Data.min) || 'Loan should be above ' + this.Data.min,
        v => (v && v <= this.Data.max) || 'Max should not be above ' + this.Data.max
      ]
    },
    retrunDateRules() {
      return [
        v => !!v || 'This field is required'

      ]
    },
    submit () {
      this.token = window.localStorage.getItem('token')

      const data = {
        loanFundTerm: this.Data.id,
        amount: this.amount,
        interestRate: this.interestRate,
        startDate: this.startDate
      }

      const requestOptions = {
        method: 'POST',
        headers: { Authorization: 'Token ' + this.token, 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }

      fetch('http://127.0.0.1:8000/loan-fund', requestOptions)
        .then(response => {
          response.json().then(data => {
            console.log(data)
            if (response.ok) {
              this.$router.push({ name: 'home' })
            }
          })
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  },
  components: {
    Amortization,
    Navbar
  }

}
</script>

<style></style>
