import { defineStore } from 'pinia'
import { transactionsAPI, budgetsAPI, goalsAPI, categoriesAPI } from '@/api/client'

export const useFinanceStore = defineStore('finance', {
  state: () => ({
    transactions: [],
    budgets: [],
    goals: [],
    categories: [],
    stats: {
      totalIncome: 0,
      totalExpenses: 0,
      balance: 0,
      monthlyIncome: 0,
      monthlyExpenses: 0,
    },
    isLoading: false,
    isTransactionsLoading: false,
    isBudgetsLoading: false,
    isGoalsLoading: false,
  }),

  getters: {
    // Transakce
    incomeTransactions: (state) => 
      state.transactions.filter(t => t.type === 'income'),
    
    expenseTransactions: (state) => 
      state.transactions.filter(t => t.type === 'expense'),
    
    recentTransactions: (state) => 
      state.transactions.slice(0, 10),
    
    // Rozpočty
    activeBudgets: (state) => 
      state.budgets.filter(b => b.is_active),
    
    budgetsByCategory: (state) => {
      const budgetMap = {}
      state.budgets.forEach(budget => {
        budgetMap[budget.category_id] = budget
      })
      return budgetMap
    },
    
    // Cíle
    activeGoals: (state) => 
      state.goals.filter(g => !g.is_completed),
    
    completedGoals: (state) => 
      state.goals.filter(g => g.is_completed),
    
    // Kategorie
    incomeCategories: (state) => 
      state.categories.filter(c => c.type === 'income'),
    
    expenseCategories: (state) => 
      state.categories.filter(c => c.type === 'expense'),
  },

  actions: {
    // Transakce
    async fetchTransactions(params = {}) {
      this.isTransactionsLoading = true
      try {
        const response = await transactionsAPI.getAll(params)
        this.transactions = response.data
      } catch (error) {
        console.error('Chyba při načítání transakcí:', error)
        throw error
      } finally {
        this.isTransactionsLoading = false
      }
    },

    async createTransaction(transaction) {
      try {
        const response = await transactionsAPI.create(transaction)
        this.transactions.unshift(response.data)
        await this.fetchStats()
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Chyba při vytváření transakce:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Chyba při vytváření transakce' 
        }
      }
    },

    async updateTransaction(id, transaction) {
      try {
        const response = await transactionsAPI.update(id, transaction)
        const index = this.transactions.findIndex(t => t.id === id)
        if (index !== -1) {
          this.transactions[index] = response.data
        }
        await this.fetchStats()
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Chyba při aktualizaci transakce:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Chyba při aktualizaci transakce' 
        }
      }
    },

    async deleteTransaction(id) {
      try {
        await transactionsAPI.delete(id)
        this.transactions = this.transactions.filter(t => t.id !== id)
        await this.fetchStats()
        return { success: true }
      } catch (error) {
        console.error('Chyba při mazání transakce:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Chyba při mazání transakce' 
        }
      }
    },

    async fetchStats() {
      try {
        const response = await transactionsAPI.getStats()
        this.stats = response.data
      } catch (error) {
        console.error('Chyba při načítání statistik:', error)
      }
    },

    // Rozpočty
    async fetchBudgets() {
      this.isBudgetsLoading = true
      try {
        const response = await budgetsAPI.getAll()
        this.budgets = response.data
      } catch (error) {
        console.error('Chyba při načítání rozpočtů:', error)
        throw error
      } finally {
        this.isBudgetsLoading = false
      }
    },

    async createBudget(budget) {
      try {
        const response = await budgetsAPI.create(budget)
        this.budgets.push(response.data)
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Chyba při vytváření rozpočtu:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Chyba při vytváření rozpočtu' 
        }
      }
    },

    async updateBudget(id, budget) {
      try {
        const response = await budgetsAPI.update(id, budget)
        const index = this.budgets.findIndex(b => b.id === id)
        if (index !== -1) {
          this.budgets[index] = response.data
        }
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Chyba při aktualizaci rozpočtu:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Chyba při aktualizaci rozpočtu' 
        }
      }
    },

    async deleteBudget(id) {
      try {
        await budgetsAPI.delete(id)
        this.budgets = this.budgets.filter(b => b.id !== id)
        return { success: true }
      } catch (error) {
        console.error('Chyba při mazání rozpočtu:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Chyba při mazání rozpočtu' 
        }
      }
    },

    // Cíle
    async fetchGoals() {
      this.isGoalsLoading = true
      try {
        const response = await goalsAPI.getAll()
        this.goals = response.data
      } catch (error) {
        console.error('Chyba při načítání cílů:', error)
        throw error
      } finally {
        this.isGoalsLoading = false
      }
    },

    async createGoal(goal) {
      try {
        const response = await goalsAPI.create(goal)
        this.goals.push(response.data)
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Chyba při vytváření cíle:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Chyba při vytváření cíle' 
        }
      }
    },

    async updateGoal(id, goal) {
      try {
        const response = await goalsAPI.update(id, goal)
        const index = this.goals.findIndex(g => g.id === id)
        if (index !== -1) {
          this.goals[index] = response.data
        }
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Chyba při aktualizaci cíle:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Chyba při aktualizaci cíle' 
        }
      }
    },

    async deleteGoal(id) {
      try {
        await goalsAPI.delete(id)
        this.goals = this.goals.filter(g => g.id !== id)
        return { success: true }
      } catch (error) {
        console.error('Chyba při mazání cíle:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Chyba při mazání cíle' 
        }
      }
    },

    // Kategorie
    async fetchCategories() {
      try {
        const response = await categoriesAPI.getAll()
        this.categories = response.data
      } catch (error) {
        console.error('Chyba při načítání kategorií:', error)
        throw error
      }
    },

    // Inicializace všech dat
    async initializeData() {
      this.isLoading = true
      try {
        await Promise.all([
          this.fetchTransactions(),
          this.fetchBudgets(),
          this.fetchGoals(),
          this.fetchCategories(),
          this.fetchStats(),
        ])
      } catch (error) {
        console.error('Chyba při inicializaci dat:', error)
      } finally {
        this.isLoading = false
      }
    },
  },
})