<template>
  <v-container fluid>
    <Navbar :username=username typeRole="bank" />
    <ListObjects  :url='FundList.url' :attribute="FundList.attribue" :actions="FundList.actions" />
  </v-container>
</template>

<script>
import Navbar from '../../components/navbar'
import ListObjects from '../../components/ListObjects'

export default {
  data: () => ({
    FundList: {
      url: process.env.VUE_APP_API_URL + '/loan-fund',
      attribue: [
        { name: 'Type', type: 'nested', DataType: 'select', parent: 'loanFundTermObject', data: { 1: 'Yearly', 2: 'Monthly', 3: 'Quarterly' } },
        { name: 'amount', type: 'number', data: '' },
        { name: 'startDate', type: 'text', data: '' },
        { name: 'endDate', type: 'text', data: '' },
        { name: 'isActive', type: 'text', data: '' }
      ],
      actions: [
        {
          name: 'Activate',
          class: 'success',
          key: 'item',
          ifFalsecondition: 'isActive',
          Function: function (item) {
            this.token = window.localStorage.getItem('token')
            const data = {
              amount: item.amount,
              startDate: item.startDate,
              endDate: item.endDate,
              isActive: true,
              provider: item.provider,
              bankPersonnal: item.bankPersonnal,
              loanFundTerm: item.loanFundTerm
            }
            const requestOptions = {
              method: 'PUT',
              headers: { Authorization: 'Token ' + this.token, 'Content-Type': 'application/json' },
              body: JSON.stringify(data)
            }
            fetch(process.env.VUE_APP_API_URL + '/loan-fund/' + item.id, requestOptions)
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
