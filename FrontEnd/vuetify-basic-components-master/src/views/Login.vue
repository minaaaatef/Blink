<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-row class="mb-12">
          <v-col cols="12">
            <h1 class="mb-5">login</h1>
            <v-divider />
          </v-col>
        </v-row>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-text-field
            v-model="username"
            :counter="10"
            :rules="nameRules"
            label="username"
            required
          ></v-text-field>

          <v-text-field
            v-model="password"
            type="password"
            label="password"
            required
          ></v-text-field>

          <v-btn color="success" class="mr-4" @click="submit">
            login
          </v-btn>
          <p class="mt-5">new user? <a @click="tosignup">signup</a></p>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  beforeCreate() {
    const myStorage = window.localStorage
    const token = myStorage.getItem('token')
    console.log(token)
    if (token !== null) {
      window.location.href = 'home'
    }
  },

  data: () => ({
    username: '',
    password: ''
  }),

  methods: {
    submit() {
      const data = {
        username: this.username,
        password: this.password
      }
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }
      fetch('http://127.0.0.1:8000/login', requestOptions)
        .then(function(response) {
          response.json().then(data => {
            console.log(data)
            window.localStorage.setItem('token', data.token)
            window.localStorage.setItem('username', data.username)
            window.localStorage.setItem('userType', data.userType)
            window.localStorage.setItem('userRoles', data.userRoles)
            window.location.href = 'home'
          })
        })
        .catch(function(error) {
          console.log(error)
        })

      console.log(data)
    },
    tosignup() {
      window.location.href = 'signup'
    }
  }
}
</script>
