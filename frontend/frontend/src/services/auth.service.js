class AuthService {
    logout() {
        localStorage.removeItem('token')
    }
}

export default new AuthService()