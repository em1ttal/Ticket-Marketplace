import http from '../http-common'

class OrderService {
  placeOrder (token, username, params) {
    const config = {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
    http.post(`/api/v1/orders/${username}`, params, config).then(r => {
      console.log(r)
    })
  }
}

export default new OrderService()
