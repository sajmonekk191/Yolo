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

      <!-- Graf příjmů a výdajů -->
      <div class="w-full">
        <!-- Měsíční trend -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Příjmy vs Výdaje</h3>
            <div class="flex items-center space-x-2">
              <div class="hidden sm:flex items-center space-x-4 mr-4">
                <div class="flex items-center space-x-2">
                  <div class="w-3 h-3 rounded-full bg-emerald-500"></div>
                  <span class="text-sm text-gray-600">Příjmy</span>
                </div>
                <div class="flex items-center space-x-2">
                  <div class="w-3 h-3 rounded-full bg-rose-500"></div>
                  <span class="text-sm text-gray-600">Výdaje</span>
                </div>
              </div>
              <select 
                v-model="trendPeriod" 
                @change="updateTrendData" 
                class="text-sm border border-gray-300 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="3">3 měsíce</option>
                <option value="6">6 měsíců</option>
                <option value="12">12 měsíců</option>
              </select>
            </div>
          </div>
          <div class="h-64 sm:h-80">
            <LineChart v-if="trendChartData && trendChartData.labels.length > 0" :data="trendChartData" :key="chartKey" />
            <div v-else class="h-full flex items-center justify-center text-gray-500">
              <div class="text-center">
                <TrendingUp class="w-12 h-12 mx-auto mb-2 text-gray-300" />
                <p class="text-sm">Zatím žádná data</p>
                <p class="text-xs mt-1">Graf se zobrazí po přidání transakcí</p>
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
            <button
              @click="openBudgetSettings"
              class="text-sm text-gray-600 hover:text-gray-900 font-medium flex items-center gap-1"
            >
              <Settings class="w-4 h-4" />
              Upravit
            </button>
          </div>
          <div v-if="financeStore.budgets.length === 0" class="text-center py-8 text-gray-500">
            <Calculator class="w-12 h-12 mx-auto mb-2 text-gray-300" />
            <p class="text-base">Zatím žádné rozpočty</p>
          </div>
          <div v-else class="space-y-3">
            <div v-for="budget in displayedBudgets" :key="budget.id">
              <div class="flex items-center justify-between mb-1">
                <div class="flex items-center space-x-2">
                  <CategoryIcon :category="budget.category" class="w-5 h-5" />
                  <span class="text-sm font-medium text-gray-900">{{ getCategoryName(budget.category) }}</span>
                </div>
                <span class="text-sm text-gray-600">
                  {{ formatCurrency(budget.spent || 0) }} / {{ formatCurrency(budget.amount) }}
                </span>
              </div>
              <div class="flex items-center gap-1">
                <div class="flex-1 bg-gray-200 rounded-full h-2 relative">
                  <div
                    class="h-2 rounded-full transition-all duration-300"
                    :class="getBudgetBarClass(budget)"
                    :style="{ width: `${Math.min(((budget.spent || 0) / budget.amount) * 100, 100)}%` }"
                  ></div>
                </div>
                <div class="flex items-center gap-1">
                  <span 
                    class="text-xs font-medium min-w-[35px] text-right"
                    :class="getBudgetPercentageClass(budget)"
                  >
                    {{ ((budget.spent || 0) / budget.amount * 100).toFixed(0) }}%
                  </span>
                  <AlertTriangle 
                    v-if="((budget.spent || 0) / budget.amount) > 1"
                    class="w-4 h-4 text-red-500 animate-pulse"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Cíle -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Finanční cíle</h3>
            <button
              @click="openGoalSettings"
              class="text-sm text-gray-600 hover:text-gray-900 font-medium flex items-center gap-1"
            >
              <Settings class="w-4 h-4" />
              Upravit
            </button>
          </div>
          <div v-if="financeStore.goals.length === 0" class="text-center py-8 text-gray-500">
            <Target class="w-12 h-12 mx-auto mb-2 text-gray-300" />
            <p class="text-base">Zatím žádné cíle</p>
          </div>
          <div v-else class="space-y-3">
            <div v-for="goal in displayedGoals" :key="goal.id" class="p-3 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center">
                    <component :is="getGoalIcon(goal.name)" class="w-4 h-4 text-white" />
                  </div>
                  <span class="text-sm font-medium text-gray-900">{{ goal.name }}</span>
                </div>
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

      <!-- Poslední transakce -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Poslední transakce</h3>
          <button
            @click="showAddTransactionModal = true"
            class="text-sm bg-indigo-600 text-white px-3 py-1.5 rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-1"
          >
            <Plus class="w-4 h-4" />
            Přidat transakci
          </button>
        </div>
        <div v-if="financeStore.recentTransactions.length === 0" class="text-center py-8 text-gray-500">
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
            v-for="transaction in financeStore.recentTransactions.slice(0, 10)"
            :key="transaction.id"
            @click="openEditTransaction(transaction)"
            class="flex items-center justify-between p-4 rounded-lg border border-gray-100 hover:border-indigo-200 hover:bg-gray-50 transition-all cursor-pointer"
          >
            <div class="flex items-center space-x-3 flex-1 min-w-0">
              <div class="flex-shrink-0">
                <p class="text-sm text-gray-500">{{ formatDate(transaction.date) }}</p>
              </div>
              <div
                class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                :class="transaction.type === 'income' 
                  ? 'bg-gradient-to-br from-emerald-400 to-teal-400' 
                  : 'bg-gradient-to-br from-rose-400 to-pink-400'"
              >
                <CategoryIcon :category="transaction.category" class="w-5 h-5 text-white" />
              </div>
              <div class="flex-1 min-w-0 ml-2">
                <p class="text-sm font-medium text-gray-900">{{ transaction.description }}</p>
                <p class="text-xs text-gray-500">{{ transaction.category }}</p>
              </div>
            </div>
            <div class="text-right flex-shrink-0 ml-4">
              <p
                class="text-lg font-semibold"
                :class="transaction.type === 'income' ? 'text-emerald-600' : 'text-rose-600'"
              >
                {{ transaction.type === 'income' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
              </p>
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

    <!-- Modal pro editaci transakce -->
    <EditTransactionModal
      v-if="showEditTransactionModal"
      :transaction="selectedTransaction"
      @close="showEditTransactionModal = false"
      @transaction-updated="handleTransactionUpdated"
    />

    <!-- Modal pro nastavení rozpočtů -->
    <div v-if="showBudgetSettings" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg max-w-md w-full max-h-[80vh] flex flex-col">
        <div class="p-6 border-b">
          <h2 class="text-lg font-semibold text-gray-900">Vyberte rozpočty pro zobrazení</h2>
          <p class="text-sm text-gray-500 mt-1">Zvolte, které rozpočty chcete vidět na dashboardu</p>
        </div>
        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-3">
            <div 
              v-for="budget in financeStore.budgets" 
              :key="budget.id"
              class="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 cursor-pointer"
              @click="toggleBudgetSelection(budget.id)"
            >
              <div class="flex items-center space-x-3">
                <div 
                  class="w-5 h-5 border-2 rounded flex items-center justify-center"
                  :class="isBudgetSelected(budget.id) ? 'bg-indigo-600 border-indigo-600' : 'border-gray-300'"
                >
                  <Check v-if="isBudgetSelected(budget.id)" class="w-3 h-3 text-white" />
                </div>
                <CategoryIcon :category="budget.category" class="w-5 h-5" />
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ getCategoryName(budget.category) }}</p>
                  <p class="text-xs text-gray-500">{{ formatCurrency(budget.spent || 0) }} / {{ formatCurrency(budget.amount) }}</p>
                </div>
              </div>
              <span 
                class="text-xs px-2 py-1 rounded-full"
                :class="getBudgetPercentageClass(budget)"
              >
                {{ ((budget.spent || 0) / budget.amount * 100).toFixed(0) }}%
              </span>
            </div>
          </div>
        </div>
        <div class="p-6 border-t flex justify-between">
          <button
            @click="selectAllBudgets"
            class="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
          >
            Vybrat vše
          </button>
          <div class="flex gap-3">
            <button
              @click="showBudgetSettings = false"
              class="px-4 py-2 text-sm text-gray-700 hover:text-gray-900"
            >
              Zrušit
            </button>
            <button
              @click="saveBudgetSettings"
              class="px-4 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            >
              Uložit
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal pro nastavení cílů -->
    <div v-if="showGoalSettings" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg max-w-md w-full max-h-[80vh] flex flex-col">
        <div class="p-6 border-b">
          <h2 class="text-lg font-semibold text-gray-900">Vyberte cíle pro zobrazení</h2>
          <p class="text-sm text-gray-500 mt-1">Zvolte, které cíle chcete vidět na dashboardu</p>
        </div>
        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-3">
            <div 
              v-for="goal in financeStore.goals" 
              :key="goal.id"
              class="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 cursor-pointer"
              @click="toggleGoalSelection(goal.id)"
            >
              <div class="flex items-center space-x-3">
                <div 
                  class="w-5 h-5 border-2 rounded flex items-center justify-center"
                  :class="isGoalSelected(goal.id) ? 'bg-indigo-600 border-indigo-600' : 'border-gray-300'"
                >
                  <Check v-if="isGoalSelected(goal.id)" class="w-3 h-3 text-white" />
                </div>
                <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center">
                  <component :is="getGoalIcon(goal.name)" class="w-4 h-4 text-white" />
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ goal.name }}</p>
                  <p class="text-xs text-gray-500">{{ formatCurrency(goal.current_amount) }} / {{ formatCurrency(goal.target_amount) }}</p>
                </div>
              </div>
              <span 
                class="text-xs px-2 py-1 rounded-full bg-purple-100 text-purple-700"
              >
                {{ ((goal.current_amount / goal.target_amount) * 100).toFixed(0) }}%
              </span>
            </div>
          </div>
        </div>
        <div class="p-6 border-t flex justify-between">
          <button
            @click="selectAllGoals"
            class="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
          >
            Vybrat vše
          </button>
          <div class="flex gap-3">
            <button
              @click="showGoalSettings = false"
              class="px-4 py-2 text-sm text-gray-700 hover:text-gray-900"
            >
              Zrušit
            </button>
            <button
              @click="saveGoalSettings"
              class="px-4 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            >
              Uložit
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
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
  Receipt,
  AlertTriangle,
  Settings,
  Check,
  Home,
  Car,
  Plane,
  GraduationCap,
  Heart,
  Smartphone,
  Gift,
  Trophy,
  Briefcase,
  DollarSign
} from 'lucide-vue-next'
import AddTransactionModal from '@/components/AddTransactionModal.vue'
import EditTransactionModal from '@/components/EditTransactionModal.vue'
import CategoryIcon from '@/components/CategoryIcon.vue'
import LineChart from '@/components/LineChart.vue'

const authStore = useAuthStore()
const financeStore = useFinanceStore()

const showAddTransactionModal = ref(false)
const showEditTransactionModal = ref(false)
const selectedTransaction = ref(null)
const showBudgetSettings = ref(false)
const showGoalSettings = ref(false)
const trendPeriod = ref('6')
const chartKey = ref(0)
const selectedBudgetIds = ref([])
const tempSelectedBudgetIds = ref([])
const selectedGoalIds = ref([])
const tempSelectedGoalIds = ref([])

const currentDate = computed(() => {
  return new Date().toLocaleDateString('cs-CZ', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const displayedBudgets = computed(() => {
  if (selectedBudgetIds.value.length === 0) {
    return financeStore.budgets.slice(0, 4)
  }
  return financeStore.budgets.filter(b => selectedBudgetIds.value.includes(b.id))
})

const displayedGoals = computed(() => {
  const activeGoals = financeStore.activeGoals
  if (selectedGoalIds.value.length === 0) {
    return activeGoals.slice(0, 3)
  }
  return activeGoals.filter(g => selectedGoalIds.value.includes(g.id))
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
    return null
  }
  
  // Skutečná data z transakcí
  const monthlyData = {}
  const monthCount = parseInt(trendPeriod.value)
  const currentDate = new Date()
  
  // Inicializace měsíců
  const monthLabels = []
  for (let i = monthCount - 1; i >= 0; i--) {
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, 1)
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    const monthName = date.toLocaleDateString('cs-CZ', { month: 'short', year: '2-digit' })
    monthLabels.push(key)
    monthlyData[key] = { 
      label: monthName,
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
  
  // Použijeme pořadí z monthLabels (chronologické)
  const labels = monthLabels.map(key => monthlyData[key].label)
  const incomeData = monthLabels.map(key => monthlyData[key].income)
  const expensesData = monthLabels.map(key => monthlyData[key].expenses)
  
  return {
    labels,
    datasets: [
      {
        label: 'Příjmy',
        data: incomeData,
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.3,
        fill: true,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: 'rgb(34, 197, 94)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2
      },
      {
        label: 'Výdaje',
        data: expensesData,
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.3,
        fill: true,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: 'rgb(239, 68, 68)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2
      }
    ]
  }
})


const getBudgetBarClass = (budget) => {
  const percentage = (budget.spent || 0) / budget.amount
  if (percentage >= 1) return 'bg-red-500'
  if (percentage >= 0.8) return 'bg-amber-500'
  if (percentage >= 0.6) return 'bg-yellow-500'
  return 'bg-emerald-500'
}

const getBudgetPercentageClass = (budget) => {
  const percentage = (budget.spent || 0) / budget.amount
  if (percentage >= 1) return 'text-red-600'
  if (percentage >= 0.8) return 'text-amber-600'
  if (percentage >= 0.6) return 'text-yellow-600'
  return 'text-gray-500'
}

const getCategoryName = (category) => {
  // Pokud je kategorie už v češtině, vrátíme ji
  if (!category) return 'Bez kategorie'
  
  // Mapování anglických názvů na české
  const categoryNames = {
    'Jídlo': 'Jídlo',
    'Nakupování': 'Nakupování', 
    'Bydlení': 'Bydlení',
    'Doprava': 'Doprava',
    'Zdraví': 'Zdraví',
    'Oblečení': 'Oblečení',
    'Zábava': 'Zábava',
    'Sport': 'Sport',
    'Cestování': 'Cestování',
    'Vzdělání': 'Vzdělání',
    'Elektronika': 'Elektronika',
    'Pojištění': 'Pojištění',
    'Energie': 'Energie',
    'Splátky': 'Splátky',
    'Ostatní': 'Ostatní',
    // Pro případ anglických názvů
    'food': 'Jídlo',
    'shopping': 'Nakupování',
    'housing': 'Bydlení',
    'transport': 'Doprava',
    'health': 'Zdraví',
    'clothing': 'Oblečení',
    'entertainment': 'Zábava',
    'sports': 'Sport',
    'travel': 'Cestování',
    'education': 'Vzdělání',
    'electronics': 'Elektronika',
    'insurance': 'Pojištění',
    'utilities': 'Energie',
    'loans': 'Splátky',
    'other': 'Ostatní'
  }
  
  return categoryNames[category] || category
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

const toggleBudgetSelection = (id) => {
  const index = tempSelectedBudgetIds.value.indexOf(id)
  if (index > -1) {
    tempSelectedBudgetIds.value.splice(index, 1)
  } else {
    tempSelectedBudgetIds.value.push(id)
  }
}

const isBudgetSelected = (id) => {
  return tempSelectedBudgetIds.value.includes(id)
}

const selectAllBudgets = () => {
  tempSelectedBudgetIds.value = financeStore.budgets.map(b => b.id)
}

const saveBudgetSettings = () => {
  selectedBudgetIds.value = [...tempSelectedBudgetIds.value]
  localStorage.setItem('selectedBudgetIds', JSON.stringify(selectedBudgetIds.value))
  showBudgetSettings.value = false
}

const getGoalIcon = (goalName) => {
  const name = goalName.toLowerCase()
  if (name.includes('dům') || name.includes('byt') || name.includes('bydlen')) return Home
  if (name.includes('auto') || name.includes('vůz')) return Car
  if (name.includes('dovolen') || name.includes('cest')) return Plane
  if (name.includes('škol') || name.includes('studium') || name.includes('vzdělán')) return GraduationCap
  if (name.includes('svatb') || name.includes('rodina')) return Heart
  if (name.includes('telefon') || name.includes('elektronik')) return Smartphone
  if (name.includes('dárek') || name.includes('vánoce')) return Gift
  if (name.includes('sport') || name.includes('fitness')) return Trophy
  if (name.includes('práce') || name.includes('podnikání')) return Briefcase
  return DollarSign
}

const toggleGoalSelection = (id) => {
  const index = tempSelectedGoalIds.value.indexOf(id)
  if (index > -1) {
    tempSelectedGoalIds.value.splice(index, 1)
  } else {
    tempSelectedGoalIds.value.push(id)
  }
}

const isGoalSelected = (id) => {
  return tempSelectedGoalIds.value.includes(id)
}

const selectAllGoals = () => {
  tempSelectedGoalIds.value = financeStore.goals.map(g => g.id)
}

const saveGoalSettings = () => {
  selectedGoalIds.value = [...tempSelectedGoalIds.value]
  localStorage.setItem('selectedGoalIds', JSON.stringify(selectedGoalIds.value))
  showGoalSettings.value = false
}

const openGoalSettings = () => {
  tempSelectedGoalIds.value = [...selectedGoalIds.value]
  showGoalSettings.value = true
}

const handleTransactionAdded = () => {
  showAddTransactionModal.value = false
  // Vynutíme re-render grafu změnou key
  chartKey.value++
}

const openEditTransaction = (transaction) => {
  selectedTransaction.value = transaction
  showEditTransactionModal.value = true
}

const handleTransactionUpdated = () => {
  showEditTransactionModal.value = false
  selectedTransaction.value = null
  // Vynutíme re-render grafu změnou key
  chartKey.value++
}

// Watch na změny transakcí pro okamžitou aktualizaci grafu
watch(() => financeStore.transactions, () => {
  // Když se změní transakce, vynutíme re-render grafu
  chartKey.value++
}, { deep: true })

// Nastaví dočasné vybrané rozpočty při otevření modalu
const openBudgetSettings = () => {
  tempSelectedBudgetIds.value = [...selectedBudgetIds.value]
  showBudgetSettings.value = true
}

const updateTrendData = () => {
  // Data se automaticky přepočítají díky computed property
  // Tato funkce je zde jen pro případné budoucí rozšíření
}

onMounted(() => {
  // Data se načtou automaticky v Layout komponentě
  
  // Načtení uložených rozpočtů
  const savedBudgets = localStorage.getItem('selectedBudgetIds')
  if (savedBudgets) {
    selectedBudgetIds.value = JSON.parse(savedBudgets)
  }
  
  // Načtení uložených cílů
  const savedGoals = localStorage.getItem('selectedGoalIds')
  if (savedGoals) {
    selectedGoalIds.value = JSON.parse(savedGoals)
  }
})
</script>

<style scoped>
.card {
  @apply bg-white rounded-xl p-4 sm:p-6 shadow-sm border border-gray-100;
}
</style>