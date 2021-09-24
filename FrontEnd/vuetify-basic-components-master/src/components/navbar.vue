<template>
  <div >
    <v-app-bar color="  accent-4" dense dark>
            <v-icon class="ma-3" @click="goTo('home')" >mdi-home</v-icon>

      <v-toolbar-title>Loan System</v-toolbar-title>

      <v-spacer></v-spacer>
          <h3 v-if="typeRole === 'bank' "  class="float-right green--text " :key="Attribute.bankAccountMoney">Balance {{Attribute.bankAccountMoney.toFixed(2)}}</h3>
            <h2 class="ma-3">{{ username }}</h2>

      <v-menu left bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item @click="logout">
            <v-list-item-title>logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
  </div>
</template>
<script>

export default {
  props: [
    'username',
    'typeRole'
  ],
  data: () => ({
    Attribute: ''
  }),
  beforeCreate() {
    const myStorage = window.localStorage
    const token = myStorage.getItem('token')
    if (token === null) {
      this.$router.push({ name: 'login' })
    }

    const requestOptions = {
      method: 'GET',
      headers: { Authorization: 'Token ' + token }
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
  methods: {
    goTo (name) {
      this.$router.push({ name: name })
    },
    submit() {
      console.log('moint')
    },
    logout() {
      const myStorage = window.localStorage
      myStorage.removeItem('token')
      this.$router.push({ name: 'login' })
    }
  }
}
</script>
