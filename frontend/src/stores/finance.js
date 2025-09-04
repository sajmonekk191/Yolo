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
      totalSavings: 0, // Součet peněz v cílech
      availableBalance: 0, // Dostupný zůstatek (bez úspor)
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
    
    recentTransactions: (state) => {
      // Transakce jsou již seřazené v fetchTransactions, jen vezmeme prvních 10
      return state.transactions.slice(0, 10)
    },
    
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
    
    // Výpočty úspor a zůstatků
    totalSavings: (state) => {
      // Součet všech peněz v cílech
      if (!state.goals || state.goals.length === 0) return 0
      return state.goals.reduce((sum, goal) => sum + (goal.current_amount || 0), 0)
    },
    
    availableBalance: (state) => {
      // Skutečný dostupný zůstatek = celkový zůstatek - peníze v cílech
      const income = state.stats?.totalIncome || 0
      const expenses = state.stats?.totalExpenses || 0
      const totalBalance = income - expenses
      const savings = state.goals?.reduce((sum, goal) => sum + (goal.current_amount || 0), 0) || 0
      return totalBalance - savings
    },
    
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
        // Seřadit transakce podle data sestupně (nejnovější první)
        this.transactions = response.data.sort((a, b) => {
          const dateA = new Date(a.date)
          const dateB = new Date(b.date)
          return dateB - dateA // Sestupně (nejnovější první)
        })
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
        // Načteme všechny transakce znovu, aby byly seřazené a měly všechny data
        await this.fetchTransactions()
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
          // Nahradíme celý objekt, aby se aktualizovaly všechny property včetně category
          this.transactions.splice(index, 1, response.data)
        }
        // Aktualizujeme také recentTransactions pro dashboard
        await this.fetchTransactions()
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
        this.stats = {
          totalIncome: response.data.total_income || 0,
          totalExpenses: response.data.total_expenses || 0,
          balance: response.data.balance || 0,
          monthlyIncome: response.data.monthly_income || 0,
          monthlyExpenses: response.data.monthly_expenses || 0,
        }
      } catch (error) {
        console.error('Chyba při načítání statistik:', error)
        // Nastavit default hodnoty při chybě
        this.stats = {
          totalIncome: 0,
          totalExpenses: 0,
          balance: 0,
          monthlyIncome: 0,
          monthlyExpenses: 0,
        }
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

    // Funkce pro přidání peněz do cíle (přesun z dostupného zůstatku)
    async addMoneyToGoal(goalId, amount) {
      try {
        const goal = this.goals.find(g => g.id === goalId)
        if (!goal) {
          return { success: false, error: 'Cíl nenalezen' }
        }
        
        // Zkontrolujeme, zda máme dostatek dostupných prostředků
        const income = this.stats?.totalIncome || 0
        const expenses = this.stats?.totalExpenses || 0
        const totalBalance = income - expenses
        const savings = this.goals?.reduce((sum, goal) => sum + (goal.current_amount || 0), 0) || 0
        const availableBalance = totalBalance - savings
        
        if (availableBalance < amount) {
          return { success: false, error: 'Nedostatek dostupných prostředků' }
        }
        
        // Aktualizujeme cíl
        const updatedGoal = {
          ...goal,
          current_amount: (goal.current_amount || 0) + amount
        }
        
        return await this.updateGoal(goalId, updatedGoal)
      } catch (error) {
        console.error('Chyba při přidávání peněz do cíle:', error)
        return { success: false, error: 'Chyba při přidávání peněz do cíle' }
      }
    },
    
    // Funkce pro výběr peněz z cíle (vrácení do dostupného zůstatku)
    async withdrawFromGoal(goalId, amount) {
      try {
        const goal = this.goals.find(g => g.id === goalId)
        if (!goal) {
          return { success: false, error: 'Cíl nenalezen' }
        }
        
        // Zkontrolujeme, zda v cíli je dostatek peněz
        if ((goal.current_amount || 0) < amount) {
          return { success: false, error: 'Nedostatek peněz v cíli' }
        }
        
        // Aktualizujeme cíl
        const updatedGoal = {
          ...goal,
          current_amount: (goal.current_amount || 0) - amount
        }
        
        return await this.updateGoal(goalId, updatedGoal)
      } catch (error) {
        console.error('Chyba při výběru peněz z cíle:', error)
        return { success: false, error: 'Chyba při výběru peněz z cíle' }
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