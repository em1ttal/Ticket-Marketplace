<template>
  <div class="page-container">
    <div class="cabecera">
      <h1>Sport Matches</h1>
      <h6 v-if="logged" style="margin-left: auto;">
        <img class="icons" src="../assets/iconUser.png" alt="User icon image"> {{ username }}
      </h6>
      <h6 v-if="logged" style="margin-left: 20px; text-align: center; margin-right: 20px">
        <img class="icons" src="../assets/moneda.png" alt="Money image"> {{ userAccount.available_money }}
      </h6>
      <button v-if="logged" class="btnVeureCistella" @click="changeCartState()">{{ textCistella }}</button>
      <button v-if="logged" class="btLogIn" @click="logOut">Log out</button>
      <button v-else class="btLogIn" style="margin-left: auto;" @click="irPaginaLogIn">Log in</button>
    </div>

    <div v-if="cart_showing" class="cart">
      <div v-if="showPurchaseSuccess" class="popup">
        <div class="popup-content">
          <p>Purchase completed successfully!</p>
          <button @click="closePopup">OK</button>
        </div>
      </div>
      <h2>Cart</h2>
      <div v-if="cart.length === 0" class="empty-cart">
        Your cart is empty.
        <div class="cart-footer">
          <button @click="changeCartState()" class="back-btn">Back</button>
        </div>
      </div>
      <div v-else>
        <table>
          <thead>
          <tr>
            <th>Sport</th>
            <th>Competition</th>
            <th>Match</th>
            <th>Quantity</th>
            <th>Price(€)</th>
            <th>Total</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(item, index) in cart" :key="index">
            <td>{{ item.sport }}</td>
            <td>{{ item.competition }}</td>
            <td>{{ item.match }}</td>
            <td class="quantity-cell">
              <button @click="decreaseQuantity(index)" class="quantity-btn">-</button>
              {{ item.quantity }}
              <button @click="increaseQuantity(index)" :disabled="totalCost() + item.price > userAccount.available_money || item.quantity >= getMatch(item.id).total_available_tickets" class="quantity-btn">+</button>
            </td>
            <td>{{ item.price.toFixed(2) }}</td>
            <td>{{ (item.price * item.quantity).toFixed(2) }}</td>
            <td>
              <button @click="removeItem(index)" class="remove-btn">Remove Ticket</button>
            </td>
          </tr>
          </tbody>
        </table>
        <div class="cart-footer">
          <button @click="changeCartState()" class="back-btn">Back</button>
          <button @click="finalizePurchase" class="purchase-btn" :disabled="totalCost() > userAccount.available_money">Purchase</button>
        </div>
      </div>
    </div>

    <div v-else class="matches">
      <div class="row">
        <div class="col-lg-4 col-md-6 mb-4" v-for="(match) in matches" :key="match.id">
          <br>
          <div class="card text-center" style="width: 18rem; margin-top: 60px">
            <img class="card-img-top" :src="require(`../assets/${match.competition.sport}.jpg`)" alt="Sports Image">
            <div class="card-body">
              <h5 class="card-title">{{ match.competition.sport }} - {{ match.competition.category }}</h5>
              <h6>{{ match.competition.name }}</h6>
              <h6>
                <strong>{{ match.local_team.name }}</strong> ({{ match.local_team.country }})<br>
                vs<br>
                <strong>{{ match.visitor_team.name }}</strong> ({{ match.visitor_team.country }})
              </h6>
              <h6>{{ match.date.substring(0, 10) }}</h6>
              <h6>{{ match.price }} &euro; </h6>
              <h6> Tickets Left: {{ match.total_available_tickets }} </h6>
              <div v-if="logged">
                <button v-if="match.price <= userAccount.available_money - totalCost() && notInCart(match) && match.total_available_tickets > 0" @click="addToCart(match)" class="btn btn-primary">Add to Cart</button>
                <button v-else-if="!notInCart(match)" class="btn btn-primary" disabled>Added</button>
                <button v-else-if="match.price > userAccount.available_money - totalCost()" class="btn btn-primary" disabled>Add to Cart</button>
                <button v-else class="btn btn-primary" disabled>Sold Out</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MatchService from '../services/MatchService'
import AuthService from '../services/AuthService'
import OrderService from '../services/OrderService'

export default {
  data () {
    return {
      matches: [],
      cart: [],
      cart_showing: false,
      logged: false,
      username: null,
      user: null,
      userAccount: null,
      textCistella: 'Open Cart',
      token: null,
      showPurchaseSuccess: false
    }
  },
  mounted () {
    this.token = this.$route.query.token
    if (this.token) {
      this.logged = this.$route.query.logged
      this.username = this.$route.query.username
      this.loadUser()
      this.loadAccount()
    }
    this.fetchMatches()
  },
  methods: {
    async fetchMatches () {
      const response = await MatchService.getAll()
      this.matches = response.data
    },
    loadUser () {
      if (this.token) {
        AuthService.getUser(this.token).then(async data => {
          this.user = data
        })
      }
    },
    loadAccount () {
      if (this.token) {
        AuthService.getUserAccount(this.token).then(async data => {
          this.userAccount = data
        })
      }
    },
    changeCartState () {
      this.cart_showing = !this.cart_showing
      this.textCistella = this.cart_showing ? 'Close Cart' : 'Open Cart'
      this.fetchMatches()
    },
    notInCart (match) {
      return !this.cart.some(item => item.id === match.id)
    },
    increaseQuantity (index) {
      const item = this.cart[index]
      const match = this.getMatch(item.id)
      if (this.totalCost() + item.price <= this.userAccount.available_money && item.quantity < match.total_available_tickets) {
        item.quantity++
      }
    },
    decreaseQuantity (index) {
      if (this.cart[index].quantity > 1) {
        this.cart[index].quantity--
      } else {
        this.removeItem(index)
      }
    },
    removeItem (index) {
      this.cart.splice(index, 1)
    },
    finalizePurchase () {
      this.cart.forEach((match) => {
        const params = {
          tickets_bought: match.quantity,
          match_id: match.id,
          account_id: this.userAccount.id,
          user_id: this.user.id
        }
        OrderService.placeOrder(this.token, this.username, params)
      })
      this.showPurchaseSuccess = true
    },
    logOut () {
      localStorage.removeItem('token')
      this.logged = false
      this.cart.length = 0
      this.userAccount.available_money = null
      this.username = null
      this.user = null
      this.userAccount = null
      this.token = null
      this.$router.push({ path: '/' })
    },
    irPaginaLogIn () {
      this.$router.push('/userlogin')
    },
    addToCart (match) {
      const cartItem = this.cart.find(item => item.id === match.id)
      if (cartItem) {
        if (this.totalCost() + cartItem.price <= this.userAccount.available_money && cartItem.quantity < match.total_available_tickets) {
          cartItem.quantity++
        }
      } else {
        if (this.totalCost() + match.price <= this.userAccount.available_money && match.total_available_tickets > 0) {
          this.cart.push({
            sport: match.competition.sport,
            competition: match.competition.name,
            match: `${match.local_team.name} vs ${match.visitor_team.name}`,
            quantity: 1,
            price: match.price,
            id: match.id
          })
        }
      }
    },
    totalCost () {
      return this.cart.reduce((total, item) => total + (item.price * item.quantity), 0)
    },
    getMatch (id) {
      return this.matches.find(match => match.id === id)
    },
    closePopup () {
      this.showPurchaseSuccess = false
      this.cart.length = 0
      this.loadAccount()
      this.fetchMatches()
    }
  }
}
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
}

.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  font-family: Arial, sans-serif;
  color: #4a4a4a;
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

.icons {
  height: 25px;
}

.cart {
  width: 90%;
  max-width: 1200px;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 160px; /* Ensure the cart is below the header */
}

h2 {
  font-size: 36px;
  margin-bottom: 20px;
  text-align: center;
}

.empty-cart {
  font-size: 24px;
  text-align: center;
  color: #4a4a4a;
  margin: 20px 0;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

th {
  background-color: #f4f4f4;
  color: #4a4a4a;
}

.quantity-cell {
  display: flex;
  align-items: center;
  justify-content: center;
}

.quantity-btn {
  padding: 5px 10px;
  font-size: 14px;
  margin: 0 5px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.quantity-btn:hover {
  background-color: #f0f0f0;
}

.remove-btn {
  padding: 5px 10px;
  font-size: 14px;
  color: white;
  background-color: #e74c3c;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.remove-btn:hover {
  background-color: #c0392b;
}

.cart-footer {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.cart-footer button {
  margin: 0 10px;
}

.back-btn, .purchase-btn {
  padding: 10px 20px;
  font-size: 16px;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-btn {
  background-color: #7f8c8d;
}

.back-btn:hover {
  background-color: #95a5a6;
}

.purchase-btn {
  background-color: #27ae60;
}

.purchase-btn:hover {
  background-color: #2ecc71;
}

.matches {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  padding-top: 160px; /* Ensure the matches start below the header */
  width: 100%; /* Ensure it takes full width */
  align-items: center; /* Align items vertically center */
}

.card.text-center {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 20px;
  padding: 20px;
  width: 100%; /* This makes the card expand to fill the column */
  max-width: 350px; /* Increase this for a larger card */
  text-align: center;
}

.col-lg-4, .col-md-6 {
  flex: 0 0 33.333333%; /* Set to one-third for three cards per row */
  max-width: 33.333333%; /* Ensure maximum width is also one-third */
  display: flex;
  justify-content: center; /* Keep this to center the cards within the columns */
}

.card img {
  width: 100%; /* Ensure the image takes full width of the card */
  border-radius: 10px;
}

.add-to-cart-btn {
  padding: 10px;
  font-size: 14px;
  color: white;
  background-color: #27ae60;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

.add-to-cart-btn:hover {
  background-color: #2ecc71;
}

.login-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  text-align: center;
}

.login-prompt p {
  font-size: 24px;
  margin-bottom: 20px;
}

.login-prompt .btLogIn,
.login-prompt .back-btn {
  font-size: 18px;
  margin: 10px;
  padding: 10px 20px;
}

.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
}

.popup-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.popup-content button {
  padding: 10px 20px;
  font-size: 16px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.popup-content button:hover {
  background: #2ecc71;
}
</style>
