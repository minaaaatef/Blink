
<template>
  <v-container>
        <h2>Amortization</h2>

  <v-simple-table>
    <template v-slot:default>

      <thead>
        <tr>

          <th class="text-left">
            number
          </th>

          <th class="text-left">
            amount
          </th>

          <th class="text-left">
            balance
          </th>

          <th class="text-left">
            interest
          </th>

          <th class="text-left">
            principal
          </th>

        </tr>
      </thead>
      <tbody>
        <tr
          v-for="item in Data.schedule"
          :key="item.name"
        >
          <td>{{ item.number }}</td>
          <td>{{ item.amount.toFixed(3) }}</td>
          <td>{{ item.balance.toFixed(3) }}</td>
          <td>{{ item.interest.toFixed(3) }}</td>
          <td>{{ item.principal.toFixed(3) }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
  </v-container>
</template>
<script>

export default {
  data: () => ({
    Data: ''
  }),

  props: [
    'url',
    'interestRate',
    'duration',
    'amount'
  ],

  beforeMount() {
    const token = window.localStorage.getItem('token')
    const data = {
      interest: this.interestRate,
      amount: this.amount,
      duration: this.duration
    }
    const requestOptions = {
      method: 'POST',
      headers: { Authorization: 'Token ' + token, 'Content-Type': 'application/json' },
      body: JSON.stringify(data)

    }
    fetch(this.url, requestOptions)
      .then(response => {
        response.json().then(data => {
          console.log(data)
          this.Data = data
        })
      }).catch(function (error) {
        console.log(error)
      })
  },
  computed: {
    headers() {
      return [
        {
          text: 'Dessert (100g serving)',
          align: 'start',
          sortable: false,
          value: 'amount'
        }
      ]
    }
  },
  methods: {
    formatPrice(value) {
      return value.toFixed(2)
    }
  }
}
</script>
