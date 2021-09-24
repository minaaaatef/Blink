<template>
  <v-container>
    <v-row>
      <v-btn color="error"      align="center"
 class="mr-4" @click="logout">
        logout
      </v-btn>
    </v-row>
  </v-container>
</template>

<script>
export default {
  methods: {
    logout() {
      const myStorage = window.localStorage
      myStorage.removeItem('token')
      myStorage.removeItem('username')
      myStorage.removeItem('userType')
      myStorage.removeItem('userRoles')
      console.log('hello')
      window.location.href = 'signup'
    }
  }
}
</script>
