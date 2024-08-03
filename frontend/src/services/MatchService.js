import http from '../http-common'

class MatchService {
  getAll () {
    return http.get('/api/v1/matches/')
      .then((res) => {
        return res.data
      })
  }
}

export default new MatchService()
