import http from '../http-common'
import axios from 'axios'

class AuthService {
  async login (username, password) {
    const parameters = 'username=' + username + '&password=' + password
    const config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }
    const path = process.env.API_URL + '/api/v1/login/access-token'

    try {
      const response = await axios.post(path, parameters, config)
      return {
        success: true,
        token: response.data.access_token
      }
    } catch (error) {
      return {
        success: false,
        message: 'Username or Password incorrect'
      }
    }
  }

  getUser (token) {
    const config = {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
    return http.get(`/api/v1/users/me`, config)
      .then(res => res.data)
  }
  async getUserAccount (token) {
    const config = {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }

    try {
      const userResponse = await http.get(`/api/v1/users/me`, config)
      const userId = userResponse.data.id
      try {
        const accountResponse = await http.get(`/api/v1/accounts/${userId}`, config)
        return accountResponse.data
      } catch (error) {
        if (error.response && error.response.status === 404) {
          console.error('Account not found:', error.response.status)
          // Handle the 404 error specifically
          return { error: 'Account not found' }
        } else {
          console.error('An error occurred while fetching the account:', error)
          // Handle other errors
          return { error: 'An error occurred while fetching the account' }
        }
      }
    } catch (error) {
      console.error('An error occurred while fetching the user:', error)
      // Handle errors while fetching the user
      return { error: 'An error occurred while fetching the user' }
    }
  }

  async signUp (email, password) {
    const fullName = email.split('@')[0]

    // Step 1: Create the user
    try {
      const userResponse = await http.post('/api/v1/users/', {
        email,
        full_name: fullName,
        password
      })

      if (userResponse.status !== 200) {
        return {
          success: false,
          message: 'User creation failed' + userResponse.statusText
        }
      }

      // Step 2: Log in to get the token
      const loginResponse = await this.login(email, password)

      if (!loginResponse.success) {
        return {
          success: false,
          message: 'Login failed after user creation' + loginResponse.statusText
        }
      }

      const token = loginResponse.token

      // Step 3: Create the account
      const config = {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }

      const accountResponse = await http.post('/api/v1/accounts/', {
        available_money: 1000,
        user_id: userResponse.data.id
      }, config)

      if (accountResponse.status !== 200) {
        return {
          success: false,
          message: 'Account creation failed' + accountResponse.statusText
        }
      }
      return {
        success: true,
        token,
        message: 'Sign Up Completed,\nAn Account Has Been Created With 1000€,\nYou Can Now LogIn'
      }
    } catch (error) {
      return {
        success: false,
        message: error
      }
    }
  }
}

export default new AuthService()
