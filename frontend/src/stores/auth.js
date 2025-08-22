import { defineStore } from 'pinia'
import { authAPI } from '@/api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isLoading: false,
    isInitialized: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
    userName: (state) => state.user?.name || '',
    userEmail: (state) => state.user?.email || '',
  },

  actions: {
    async login(credentials) {
      this.isLoading = true
      try {
        const response = await authAPI.login(credentials)
        const { access_token, token_type } = response.data
        
        this.token = access_token
        
        localStorage.setItem('token', access_token)
        
        // Načíst data uživatele
        await this.checkAuth()
        
        return { success: true }
      } catch (error) {
        console.error('Chyba při přihlašování:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Chyba při přihlašování' 
        }
      } finally {
        this.isLoading = false
      }
    },

    async register(userData) {
      this.isLoading = true
      try {
        await authAPI.register(userData)
        return { success: true }
      } catch (error) {
        console.error('Chyba při registraci:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Chyba při registraci' 
        }
      } finally {
        this.isLoading = false
      }
    },

    async checkAuth() {
      if (!this.token) {
        this.isInitialized = true
        return
      }

      try {
        const response = await authAPI.getCurrentUser()
        this.user = response.data
      } catch (error) {
        console.error('Chyba při ověřování uživatele:', error)
        this.logout()
      } finally {
        this.isInitialized = true
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    // Načtení uživatele z localStorage při startu
    initializeAuth() {
      const savedUser = localStorage.getItem('user')
      const savedToken = localStorage.getItem('token')
      
      if (savedUser && savedToken) {
        try {
          this.user = JSON.parse(savedUser)
          this.token = savedToken
        } catch (error) {
          console.error('Chyba při načítání uložených dat:', error)
          this.logout()
        }
      }
    },
  },
})