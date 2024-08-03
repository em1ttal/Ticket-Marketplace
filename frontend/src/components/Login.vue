<template>
  <div class="login-container">
    <div class="cabecera">
      <h1>Sport Matches</h1>
    </div>
    <div class="login-card">
      <h2 class="text-center">Sign In</h2>
      <form>
        <div class="form-label-group">
          <label for="inputUsername">Username</label>
          <input type="text" id="inputUsername" class="form-control" placeholder="Username" required autofocus v-model="username">
        </div>
        <div class="form-label-group">
          <label for="inputPassword">Password</label>
          <input type="password" id="inputPassword" class="form-control" placeholder="Password" required v-model="password">
        </div>
        <div class="button-group">
          <b-button @click="login_user" variant="primary" block>Sign In</b-button>
          <b-button @click="register_user" variant="success" block>Create Account</b-button>
          <b-button @click="back_matches" variant="secondary" block>Back To Matches</b-button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import AuthService from '../services/AuthService'

export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: '',
      token: '',
      logged: false
    }
  },
  methods: {
    async login_user (event) {
      event.preventDefault()
      const result = await AuthService.login(this.username, this.password)
      if (result.success) {
        this.logged = true
        this.token = result.token
        await this.$router.push({
          path: '/',
          query: {
            username: this.username,
            logged: this.logged,
            token: this.token
          }
        })
      } else {
        alert(result.message)
      }
    },
    async register_user (event) {
      // Handle register action
      if (this.username === '' || this.password === '') {
        alert('Username and password are required')
        return
      }
      const result = await AuthService.signUp(this.username, this.password)
      if (result.success) {
        alert(result.message)
      } else {
        alert(result.message)
      }
    },
    back_matches (event) {
      // Handle back to matches action
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #faebd7;
}

.cabecera {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  align-items: center;
  background-color: white;
  height: 100px;
  padding: 40px;
  border-bottom: 1px solid black;
  box-sizing: border-box;
  z-index: 1000; /* Ensure the header stays on top */
}

.login-card {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 500px; /* Increased width */
  text-align: left; /* Changed to left align */
  margin-top: 40px; /* Added margin to separate from header */
}

.form-label-group {
  margin-bottom: 20px;
}

.form-label-group label {
  display: block;
  margin-bottom: 5px;
}

.button-group {
  display: flex;
  flex-direction: column;
}

.button-group .btn {
  margin-bottom: 10px;
}
</style>
