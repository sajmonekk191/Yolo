<template>
  <div class="space-y-6">
    <!-- Nadpis -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">Přehled</h1>
        <p class="text-sm sm:text-base text-gray-600">Vítejte zpět, {{ authStore.userName }}!</p>
      </div>
      <div class="text-xs sm:text-sm text-gray-500">
        {{ currentDate }}
      </div>
    </div>

    <!-- Loading stav -->
    <div v-if="financeStore.isLoading" class="flex items-center justify-center py-12">
      <div class="loading-spinner"></div>
    </div>

    <div v-else class="space-y-6">
      <!-- Finanční statistiky -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <!-- Celkový zůstatek -->
        <div class="card bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white shadow-lg sm:col-span-2 lg:col-span-1">
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0">
              <p class="text-indigo-100 text-xs sm:text-sm font-medium opacity-90">Celkový zůstatek</p>
              <p class="text-2xl sm:text-3xl font-bold truncate">{{ formatCurrency(financeStore.stats.balance) }}</p>
              <p class="text-xs text-indigo-100 mt-1 opacity-75">
                {{ balanceChange >= 0 ? '+' : '' }}{{ formatCurrency(balanceChange) }} tento měsíc
              </p>
            </div>
            <div class="w-12 h-12 sm:w-14 sm:h-14 bg-white bg-opacity-20 backdrop-blur rounded-xl flex items-center justify-center flex-shrink-0 ml-3">
              <Wallet class="w-6 h-6 sm:w-7 sm:h-7" />
            </div>
          </div>
        </div>

        <!-- Měsíční příjmy -->
        <div class="card bg-gradient-to-br from-emerald-50 to-teal-50 border-0">
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0">
              <p class="text-gray-600 text-xs sm:text-sm font-medium">Měsíční příjmy</p>
              <p class="text-xl sm:text-2xl font-bold text-emerald-600 truncate">{{ formatCurrency(financeStore.stats.monthlyIncome) }}</p>
              <div class="flex items-center mt-1">
                <TrendingUp v-if="incomeChange >= 0" class="w-3 h-3 text-emerald-500 mr-1" />
                <TrendingDown v-else class="w-3 h-3 text-red-500 mr-1" />
                <span class="text-xs" :class="incomeChange >= 0 ? 'text-emerald-600' : 'text-red-600'">
                  {{ Math.abs(incomeChange).toFixed(1) }}% oproti minulému měsíci
                </span>
              </div>
            </div>
            <div class="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-emerald-400 to-teal-400 rounded-xl flex items-center justify-center flex-shrink-0 ml-3 shadow-lg">
              <TrendingUp class="w-6 h-6 sm:w-7 sm:h-7 text-white" />
            </div>
          </div>
        </div>

        <!-- Měsíční výdaje -->
        <div class="card bg-gradient-to-br from-rose-50 to-pink-50 border-0">
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0">
              <p class="text-gray-600 text-xs sm:text-sm font-medium">Měsíční výdaje</p>
              <p class="text-xl sm:text-2xl font-bold text-rose-600 truncate">{{ formatCurrency(financeStore.stats.monthlyExpenses) }}</p>
              <div class="flex items-center mt-1">
                <TrendingDown v-if="expenseChange <= 0" class="w-3 h-3 text-emerald-500 mr-1" />
                <TrendingUp v-else class="w-3 h-3 text-red-500 mr-1" />
                <span class="text-xs" :class="expenseChange <= 0 ? 'text-emerald-600' : 'text-red-600'">
                  {{ Math.abs(expenseChange).toFixed(1) }}% oproti minulému měsíci
                </span>
              </div>
            </div>
            <div class="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-rose-400 to-pink-400 rounded-xl flex items-center justify-center flex-shrink-0 ml-3 shadow-lg">
              <TrendingDown class="w-6 h-6 sm:w-7 sm:h-7 text-white" />
            </div>
          </div>
        </div>

        <!-- Úspory -->
        <div class="card bg-gradient-to-br from-amber-50 to-orange-50 border-0 sm:col-span-2 lg:col-span-1">
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0">
              <p class="text-gray-600 text-xs sm:text-sm font-medium">Měsíční úspory</p>
              <p class="text-xl sm:text-2xl font-bold text-amber-600 truncate">
                {{ formatCurrency(financeStore.stats.monthlyIncome - financeStore.stats.monthlyExpenses) }}
              </p>
              <div class="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                <div
                  class="bg-gradient-to-r from-amber-400 to-orange-400 h-1.5 rounded-full transition-all duration-300"
                  :style="{ width: `${savingsRate}%` }"
                ></div>
              </div>
              <p class="text-xs text-gray-500 mt-1">{{ savingsRate.toFixed(1) }}% míra úspor</p>
            </div>
            <div class="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-amber-400 to-orange-400 rounded-xl flex items-center justify-center flex-shrink-0 ml-3 shadow-lg">
              <PiggyBank class="w-6 h-6 sm:w-7 sm:h-7 text-white" />
            </div>
          </div>
        </div>
      </div>

      <!-- Grafy a diagramy -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        <!-- Měsíční trend -->
        <div class="card lg:col-span-2">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Příjmy vs Výdaje</h3>
            <select v-model="trendPeriod" @change="updateTrendData" class="text-sm border-gray-300 rounded-lg px-3 py-1.5">
              <option value="3">Poslední 3 měsíce</option>
              <option value="6">Posledních 6 měsíců</option>
              <option value="12">Poslední rok</option>
            </select>
          </div>
          <div class="h-64 sm:h-80">
            <LineChart v-if="trendChartData" :data="trendChartData" />
          </div>
        </div>

        <!-- Kategorie výdajů -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Rozložení výdajů</h3>
          <div class="h-64 sm:h-80">
            <DoughnutChart v-if="categoryChartData && categoryChartData.labels.length > 0" :data="categoryChartData" />
            <div v-else class="h-full flex items-center justify-center text-gray-500">
              <div class="text-center">
                <PieChart class="w-12 h-12 mx-auto mb-2 text-gray-300" />
                <p class="text-sm">Zatím žádné výdaje</p>
                <p class="text-xs mt-1">Data se zobrazí po přidání transakcí</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Rozpočty a cíle -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <!-- Rozpočty -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Rozpočty</h3>
            <router-link to="/rozpocty" class="text-sm text-indigo-600 hover:text-indigo-500 font-medium">
              Zobrazit vše
            </router-link>
          </div>
          <div v-if="financeStore.budgets.length === 0" class="text-center py-8 text-gray-500">
            <Calculator class="w-12 h-12 mx-auto mb-2 text-gray-300" />
            <p class="text-base">Zatím žádné rozpočty</p>
          </div>
          <div v-else class="space-y-3">
            <div v-for="budget in financeStore.budgets.slice(0, 4)" :key="budget.id" class="space-y-2">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <CategoryIcon :category="budget.category" class="w-5 h-5" />
                  <span class="text-sm font-medium text-gray-900">{{ budget.category }}</span>
                </div>
                <span class="text-sm text-gray-600">
                  {{ formatCurrency(budget.spent || 0) }} / {{ formatCurrency(budget.amount) }}
                </span>
              </div>
              <div class="relative">
                <div class="w-full bg-gray-200 rounded-full h-2 mb-1">
                  <div
                    class="h-2 rounded-full transition-all duration-300"
                    :class="getBudgetBarClass(budget)"
                    :style="{ width: `${Math.min(((budget.spent || 0) / budget.amount) * 100, 100)}%` }"
                  ></div>
                </div>
                <div class="text-right">
                  <span class="text-xs text-gray-500">
                    {{ ((budget.spent || 0) / budget.amount * 100).toFixed(0) }}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Cíle -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Finanční cíle</h3>
            <router-link to="/cile" class="text-sm text-indigo-600 hover:text-indigo-500 font-medium">
              Zobrazit vše
            </router-link>
          </div>
          <div v-if="financeStore.goals.length === 0" class="text-center py-8 text-gray-500">
            <Target class="w-12 h-12 mx-auto mb-2 text-gray-300" />
            <p class="text-base">Zatím žádné cíle</p>
          </div>
          <div v-else class="space-y-3">
            <div v-for="goal in financeStore.activeGoals.slice(0, 3)" :key="goal.id" class="p-3 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-gray-900">{{ goal.name }}</span>
                <span class="text-xs px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full">
                  {{ daysUntilDeadline(goal.deadline) }} dní
                </span>
              </div>
              <div class="w-full bg-white rounded-full h-2 mb-1">
                <div
                  class="bg-gradient-to-r from-purple-500 to-indigo-500 h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${Math.min((goal.current_amount / goal.target_amount) * 100, 100)}%` }"
                ></div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">
                  {{ formatCurrency(goal.current_amount) }} z {{ formatCurrency(goal.target_amount) }}
                </span>
                <span class="text-xs font-medium text-indigo-600">
                  {{ ((goal.current_amount / goal.target_amount) * 100).toFixed(0) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Rychlé akce a poslední transakce -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        <!-- Rychlé akce -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Rychlé akce</h3>
          <div class="grid grid-cols-2 gap-3">
            <button
              @click="showAddTransactionModal = true"
              class="flex flex-col items-center p-4 rounded-xl border-2 border-dashed border-gray-300 hover:border-indigo-500 hover:bg-indigo-50 transition-all group"
            >
              <div class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center mb-2 group-hover:bg-indigo-200">
                <Plus class="w-5 h-5 text-indigo-600" />
              </div>
              <span class="text-sm font-medium text-gray-700 group-hover:text-indigo-600">Transakce</span>
            </button>
            <router-link
              to="/cile"
              class="flex flex-col items-center p-4 rounded-xl border-2 border-dashed border-gray-300 hover:border-purple-500 hover:bg-purple-50 transition-all group"
            >
              <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mb-2 group-hover:bg-purple-200">
                <Target class="w-5 h-5 text-purple-600" />
              </div>
              <span class="text-sm font-medium text-gray-700 group-hover:text-purple-600">Nový cíl</span>
            </router-link>
            <router-link
              to="/rozpocty"
              class="flex flex-col items-center p-4 rounded-xl border-2 border-dashed border-gray-300 hover:border-amber-500 hover:bg-amber-50 transition-all group"
            >
              <div class="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center mb-2 group-hover:bg-amber-200">
                <Calculator class="w-5 h-5 text-amber-600" />
              </div>
              <span class="text-sm font-medium text-gray-700 group-hover:text-amber-600">Rozpočet</span>
            </router-link>
            <button
              @click="exportData"
              class="flex flex-col items-center p-4 rounded-xl border-2 border-dashed border-gray-300 hover:border-teal-500 hover:bg-teal-50 transition-all group"
            >
              <div class="w-10 h-10 bg-teal-100 rounded-lg flex items-center justify-center mb-2 group-hover:bg-teal-200">
                <Download class="w-5 h-5 text-teal-600" />
              </div>
              <span class="text-sm font-medium text-gray-700 group-hover:text-teal-600">Export</span>
            </button>
          </div>
        </div>

        <!-- Poslední transakce -->
        <div class="card lg:col-span-2">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Poslední transakce</h3>
            <router-link to="/transakce" class="text-sm text-indigo-600 hover:text-indigo-500 font-medium">
              Zobrazit vše
            </router-link>
          </div>
          <div v-if="financeStore.recentTransactions.length === 0" class="text-center py-6 text-gray-500">
            <Receipt class="w-12 h-12 mx-auto mb-2 text-gray-300" />
            <p class="text-base">Zatím žádné transakce</p>
            <button
              @click="showAddTransactionModal = true"
              class="mt-2 text-sm text-indigo-600 hover:text-indigo-500 font-medium"
            >
              Přidat první transakci
            </button>
          </div>
          <div v-else class="space-y-2">
            <div
              v-for="transaction in financeStore.recentTransactions"
              :key="transaction.id"
              class="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-center space-x-3 flex-1 min-w-0">
                <div
                  class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                  :class="transaction.type === 'income' 
                    ? 'bg-gradient-to-br from-emerald-400 to-teal-400' 
                    : 'bg-gradient-to-br from-rose-400 to-pink-400'"
                >
                  <CategoryIcon :category="transaction.category" class="w-5 h-5 text-white" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ transaction.description }}</p>
                  <p class="text-xs text-gray-500">{{ transaction.category }} • {{ formatDate(transaction.date) }}</p>
                </div>
              </div>
              <div class="text-right flex-shrink-0 ml-2">
                <p
                  class="text-base font-semibold"
                  :class="transaction.type === 'income' ? 'text-emerald-600' : 'text-rose-600'"
                >
                  {{ transaction.type === 'income' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal pro přidání transakce -->
    <AddTransactionModal
      v-if="showAddTransactionModal"
      @close="showAddTransactionModal = false"
      @transaction-added="handleTransactionAdded"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useFinanceStore } from '@/stores/finance'
import {
  Wallet,
  TrendingUp,
  TrendingDown,
  Target,
  Plus,
  PiggyBank,
  Calculator,
  Download,
  Receipt,
  PieChart
} from 'lucide-vue-next'
import AddTransactionModal from '@/components/AddTransactionModal.vue'
import CategoryIcon from '@/components/CategoryIcon.vue'
import LineChart from '@/components/LineChart.vue'
import DoughnutChart from '@/components/DoughnutChart.vue'

const authStore = useAuthStore()
const financeStore = useFinanceStore()

const showAddTransactionModal = ref(false)
const trendPeriod = ref('6')

const currentDate = computed(() => {
  return new Date().toLocaleDateString('cs-CZ', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

// Simulované hodnoty změn
const balanceChange = computed(() => {
  return financeStore.stats.monthlyIncome - financeStore.stats.monthlyExpenses
})

const incomeChange = ref(12.5)
const expenseChange = ref(-5.3)

const savingsRate = computed(() => {
  if (financeStore.stats.monthlyIncome === 0) return 0
  const rate = ((financeStore.stats.monthlyIncome - financeStore.stats.monthlyExpenses) / financeStore.stats.monthlyIncome) * 100
  return Math.max(0, Math.min(100, rate))
})

// Data pro grafy
const trendChartData = computed(() => {
  if (!financeStore.transactions || financeStore.transactions.length === 0) {
    // Pokud nejsou data, vrátíme simulovaná
    const months = []
    const income = []
    const expenses = []
    
    const monthCount = parseInt(trendPeriod.value)
    const currentDate = new Date()
    
    for (let i = monthCount - 1; i >= 0; i--) {
      const date = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, 1)
      months.push(date.toLocaleDateString('cs-CZ', { month: 'short' }))
      
      // Demo data
      income.push(Math.floor(Math.random() * 20000 + 40000))
      expenses.push(Math.floor(Math.random() * 15000 + 25000))
    }
    
    return {
      labels: months,
      datasets: [
        {
          label: 'Příjmy',
          data: income,
          borderColor: 'rgb(16, 185, 129)',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          tension: 0.4,
          fill: true
        },
        {
          label: 'Výdaje',
          data: expenses,
          borderColor: 'rgb(244, 63, 94)',
          backgroundColor: 'rgba(244, 63, 94, 0.1)',
          tension: 0.4,
          fill: true
        }
      ]
    }
  }
  
  // Skutečná data z transakcí
  const monthlyData = {}
  const monthCount = parseInt(trendPeriod.value)
  const currentDate = new Date()
  
  // Inicializace měsíců
  for (let i = monthCount - 1; i >= 0; i--) {
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, 1)
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    monthlyData[key] = { 
      label: date.toLocaleDateString('cs-CZ', { month: 'short' }),
      income: 0, 
      expenses: 0 
    }
  }
  
  // Zpracování transakcí
  financeStore.transactions.forEach(transaction => {
    const date = new Date(transaction.date)
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    
    if (monthlyData[key]) {
      if (transaction.type === 'income') {
        monthlyData[key].income += transaction.amount
      } else {
        monthlyData[key].expenses += transaction.amount
      }
    }
  })
  
  // Převod na pole pro graf
  const sortedMonths = Object.keys(monthlyData).sort()
  const labels = sortedMonths.map(key => monthlyData[key].label)
  const incomeData = sortedMonths.map(key => monthlyData[key].income)
  const expensesData = sortedMonths.map(key => monthlyData[key].expenses)
  
  return {
    labels,
    datasets: [
      {
        label: 'Příjmy',
        data: incomeData,
        borderColor: 'rgb(16, 185, 129)',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.4,
        fill: true
      },
      {
        label: 'Výdaje',
        data: expensesData,
        borderColor: 'rgb(244, 63, 94)',
        backgroundColor: 'rgba(244, 63, 94, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  }
})

const categoryChartData = computed(() => {
  const categoryTotals = {}
  
  if (!financeStore.transactions || financeStore.transactions.length === 0) {
    return null
  }
  
  financeStore.transactions
    .filter(t => t.type === 'expense')
    .forEach(t => {
      if (t.category && t.category !== 'undefined') {
        categoryTotals[t.category] = (categoryTotals[t.category] || 0) + t.amount
      }
    })
  
  const labels = Object.keys(categoryTotals)
  const data = Object.values(categoryTotals)
  
  if (labels.length === 0) {
    return null
  }
  
  return {
    labels,
    datasets: [{
      data,
      backgroundColor: [
        'rgb(99, 102, 241)',
        'rgb(168, 85, 247)',
        'rgb(236, 72, 153)',
        'rgb(251, 146, 60)',
        'rgb(250, 204, 21)',
        'rgb(34, 197, 94)',
        'rgb(20, 184, 166)',
        'rgb(59, 130, 246)'
      ],
      borderWidth: 0
    }]
  }
})

const getBudgetBarClass = (budget) => {
  const percentage = (budget.spent || 0) / budget.amount
  if (percentage >= 1) return 'bg-red-500'
  if (percentage >= 0.8) return 'bg-amber-500'
  if (percentage >= 0.6) return 'bg-yellow-500'
  return 'bg-emerald-500'
}

const daysUntilDeadline = (deadline) => {
  const today = new Date()
  const deadlineDate = new Date(deadline)
  const diffTime = deadlineDate - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return Math.max(0, diffDays)
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('cs-CZ', {
    style: 'currency',
    currency: 'CZK',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount || 0)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('cs-CZ')
}

const handleTransactionAdded = () => {
  showAddTransactionModal.value = false
}

const updateTrendData = () => {
  // Tato funkce se zavolá při změně období
  // Data se automaticky přepočítají díky computed
}

const exportData = () => {
  // Implementace exportu dat
  alert('Export dat bude implementován')
}

onMounted(() => {
  // Data se načtou automaticky v Layout komponentě
})
</script>

<style scoped>
.card {
  @apply bg-white rounded-xl p-4 sm:p-6 shadow-sm border border-gray-100;
}
</style>