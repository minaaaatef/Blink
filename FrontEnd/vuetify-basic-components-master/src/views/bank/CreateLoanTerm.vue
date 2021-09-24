<template>
  <v-card class="mt-8">
    <v-card-title>
      Create Loan Term
    </v-card-title>
    <v-card-text>
      Create New Loan Term
      <v-form>
        <v-select
          v-model="type"
          :items="typeSelect"
          :item-text="text"
          :item-value="value"
          :rules="[v => !!v || 'Item is required']"
          label="Fund Type"
          required
        ></v-select>
        <v-text-field
          v-model="max"
          label="MAX"
          required
          type="number"
        ></v-text-field>
        <v-text-field
          v-model="min"
          label="MIN"
          required
          type="number"
        ></v-text-field>
        <v-text-field
          v-model="interestRate"
          label="interestRate %"
          required
          type="number"
        ></v-text-field>
        <v-text-field
          v-model="BankProfitRate"
          label="BankProfitRate %"
          required
          type="number"
        ></v-text-field>
        <v-text-field
          v-model="RiskRate"
          label="RiskRate %"
          required
          type="number"
        ></v-text-field>
        <v-text-field
          v-model="duration"
          label="duration"
          required
          type="number"

        ></v-text-field>
        <v-btn class="success" @click="submit">Submit</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
export default {

  data: () => ({
    typeSelect: [
      {
        text: 'Yearly',
        value: 1
      },
      {
        text: 'Monthly',
        value: 2
      },
      {
        text: 'Quarterly',
        value: 3
      }
    ],
    type: '',
    max: '',
    min: '',
    interestRate: '',
    RiskRate: '',
    BankProfitRate: '',
    duration: '',
    token: ''
  }),
  mounted() {
    this.token = window.localStorage.getItem('token')

    const requestOptions = {
      method: 'GET',
      headers: { Authorization: 'Token ' + this.token }
    }

    fetch(process.env.VUE_APP_API_URL + '/Attribute', requestOptions)
      .then(response => {
        response.json().then(data => {
          console.log(data)
          this.interestRate = data.interestRate
          this.BankProfitRate = data.BankProfitRate
          this.RiskRate = data.RiskRate
        })
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  methods: {
    submit() {
      this.token = window.localStorage.getItem('token')
      const data = {
        max: this.max,
        min: this.min,
        interestRate: this.interestRate,
        duration: this.duration,
        Type: this.type

      }
      const requestOptions = {
        method: 'POST',
        headers: { Authorization: 'Token ' + this.token, 'Content-Type': 'application/json' },
        body: JSON.stringify(data)

      }

      fetch(process.env.VUE_APP_API_URL + '/loan-term', requestOptions)
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
  }
}
</script>
