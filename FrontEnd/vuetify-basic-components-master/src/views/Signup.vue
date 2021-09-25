<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-row class="mb-12">
          <v-col cols="12">
            <h1 class="mb-5">sign up</h1>
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
            v-model="email"
            :rules="emailRules"
            label="E-mail"
            required
          ></v-text-field>

          <v-text-field
            v-model="password"
            type="password"
            label="password"
            required
          ></v-text-field>

          <v-select
            v-model="type"
            :items="typeSelect"
            :item-text="text"
            :item-value="value"
            :rules="[v => !!v || 'Role is required']"
            label="Role"
            required
          ></v-select>
          <v-btn color="success" class="mr-4" @click="submit">
            submit
          </v-btn>
          <p>Already a user? <a @click="toLogin">Login</a></p>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
  mounted() {
    const myStorage = window.localStorage
    const token = myStorage.getItem('token')
    console.log(token)
    if (token !== null) {
      window.location.href = 'home'
    }
  },

  data: () => ({
    valid: true,
    username: '',
    nameRules: [
      v => !!v || 'Name is required',
      v => (v && v.length <= 10) || 'Name must be less than 10 characters'
    ],
    email: '',
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
    ],
    type: null,
    typeSelect: [
      {
        text: 'loan provider',
        value: 1
      },
      {
        text: 'Loan Customers',
        value: 2
      }
    ],
    password: ''
  }),

  methods: {
    submit() {
      const data = {
        username: this.username,
        password: this.password,
        email: this.email,
        type: this.type
      }

      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }

      fetch('http://127.0.0.1:8000/register', requestOptions)
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
    toLogin() {
      window.location.href = 'login'
    }
  }
}
</script>
