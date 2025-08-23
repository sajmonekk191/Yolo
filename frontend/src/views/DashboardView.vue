<template>
  <div class="space-y-6">
    <!-- Nadpis -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-gray-900">Přehled</h1>
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
        <div class="card bg-gradient-to-r from-blue-600 to-indigo-600 text-white sm:col-span-2 lg:col-span-1">
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0">
              <p class="text-blue-100 text-xs sm:text-sm font-medium">Celkový zůstatek</p>
              <p class="text-lg sm:text-xl lg:text-2xl font-bold truncate">{{ formatCurrency(financeStore.stats.balance) }}</p>
            </div>
            <div class="w-10 h-10 sm:w-12 sm:h-12 bg-white bg-opacity-20 rounded-lg flex items-center justify-center flex-shrink-0 ml-3">
              <Wallet class="w-5 h-5 sm:w-6 sm:h-6" />
            </div>
          </div>
        </div>

        <!-- Měsíční příjmy -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0">
              <p class="text-gray-600 text-xs sm:text-sm font-medium">Měsíční příjmy</p>
              <p class="text-lg sm:text-xl lg:text-2xl font-bold text-green-600 truncate">{{ formatCurrency(financeStore.stats.monthlyIncome) }}</p>
            </div>
            <div class="w-10 h-10 sm:w-12 sm:h-12 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0 ml-3">
              <TrendingUp class="w-5 h-5 sm:w-6 sm:h-6 text-green-600" />
            </div>
          </div>
        </div>

        <!-- Měsíční výdaje -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0">
              <p class="text-gray-600 text-xs sm:text-sm font-medium">Měsíční výdaje</p>
              <p class="text-lg sm:text-xl lg:text-2xl font-bold text-red-600 truncate">{{ formatCurrency(financeStore.stats.monthlyExpenses) }}</p>
            </div>
            <div class="w-10 h-10 sm:w-12 sm:h-12 bg-red-100 rounded-lg flex items-center justify-center flex-shrink-0 ml-3">
              <TrendingDown class="w-5 h-5 sm:w-6 sm:h-6 text-red-600" />
            </div>
          </div>
        </div>

        <!-- Aktivní cíle -->
        <div class="card sm:col-span-2 lg:col-span-1">
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0">
              <p class="text-gray-600 text-xs sm:text-sm font-medium">Aktivní cíle</p>
              <p class="text-lg sm:text-xl lg:text-2xl font-bold text-purple-600">{{ financeStore.activeGoals.length }}</p>
            </div>
            <div class="w-10 h-10 sm:w-12 sm:h-12 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0 ml-3">
              <Target class="w-5 h-5 sm:w-6 sm:h-6 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      <!-- Grafy a diagramy -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <!-- Měsíční trend -->
        <div class="card">
          <h3 class="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Měsíční trend</h3>
          <div class="h-48 sm:h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <div class="text-center text-gray-500">
              <BarChart3 class="w-10 h-10 sm:w-12 sm:h-12 mx-auto mb-2" />
              <p class="text-sm sm:text-base">Graf bude implementován</p>
              <p class="text-xs sm:text-sm">pomocí Chart.js</p>
            </div>
          </div>
        </div>

        <!-- Kategorie výdajů -->
        <div class="card">
          <h3 class="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Kategorie výdajů</h3>
          <div class="h-48 sm:h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <div class="text-center text-gray-500">
              <PieChart class="w-10 h-10 sm:w-12 sm:h-12 mx-auto mb-2" />
              <p class="text-sm sm:text-base">Koláčový graf</p>
              <p class="text-xs sm:text-sm">kategorie výdajů</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Rychlé akce a přehled -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        <!-- Rychlé akce -->
        <div class="card">
          <h3 class="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Rychlé akce</h3>
          <div class="space-y-2 sm:space-y-3">
            <button
              @click="showAddTransactionModal = true"
              class="flex items-center space-x-3 w-full p-2.5 sm:p-3 rounded-lg border border-gray-200 hover:bg-gray-50 active:bg-gray-100 transition-colors"
            >
              <div class="w-7 h-7 sm:w-8 sm:h-8 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <Plus class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-green-600" />
              </div>
              <span class="text-sm sm:text-base font-medium text-gray-900">Přidat transakci</span>
            </button>
            <router-link
              to="/cile"
              class="flex items-center space-x-3 w-full p-2.5 sm:p-3 rounded-lg border border-gray-200 hover:bg-gray-50 active:bg-gray-100 transition-colors"
            >
              <div class="w-7 h-7 sm:w-8 sm:h-8 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <Target class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-purple-600" />
              </div>
              <span class="text-sm sm:text-base font-medium text-gray-900">Nový cíl</span>
            </router-link>
            <router-link
              to="/rozpocty"
              class="flex items-center space-x-3 w-full p-2.5 sm:p-3 rounded-lg border border-gray-200 hover:bg-gray-50 active:bg-gray-100 transition-colors"
            >
              <div class="w-7 h-7 sm:w-8 sm:h-8 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <PiggyBank class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-blue-600" />
              </div>
              <span class="text-sm sm:text-base font-medium text-gray-900">Nový rozpočet</span>
            </router-link>
          </div>
        </div>

        <!-- Poslední transakce -->
        <div class="card lg:col-span-2">
          <div class="flex items-center justify-between mb-3 sm:mb-4">
            <h3 class="text-base sm:text-lg font-semibold text-gray-900">Poslední transakce</h3>
            <router-link
              to="/transakce"
              class="text-xs sm:text-sm text-blue-600 hover:text-blue-500 font-medium"
            >
              Zobrazit vše
            </router-link>
          </div>
          <div v-if="financeStore.recentTransactions.length === 0" class="text-center py-4 sm:py-6 text-gray-500">
            <ArrowUpDown class="w-10 h-10 sm:w-12 sm:h-12 mx-auto mb-2 text-gray-300" />
            <p class="text-sm sm:text-base">Zatím žádné transakce</p>
            <button
              @click="showAddTransactionModal = true"
              class="mt-2 text-xs sm:text-sm text-blue-600 hover:text-blue-500 font-medium"
            >
              Přidat první transakci
            </button>
          </div>
          <div v-else class="space-y-2 sm:space-y-3">
            <div
              v-for="transaction in financeStore.recentTransactions"
              :key="transaction.id"
              class="flex items-center justify-between p-2.5 sm:p-3 rounded-lg border border-gray-100 hover:bg-gray-50"
            >
              <div class="flex items-center space-x-2 sm:space-x-3 flex-1 min-w-0">
                <div
                  class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                  :class="transaction.type === 'income' ? 'bg-green-100' : 'bg-red-100'"
                >
                  <ArrowUpDown
                    class="w-4 h-4 sm:w-5 sm:h-5"
                    :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'"
                  />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm sm:text-base font-medium text-gray-900 truncate">{{ transaction.description }}</p>
                  <p class="text-xs sm:text-sm text-gray-500">{{ transaction.category }}</p>
                </div>
              </div>
              <div class="text-right flex-shrink-0 ml-2">
                <p
                  class="text-sm sm:text-base font-semibold"
                  :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'"
                >
                  {{ transaction.type === 'income' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
                </p>
                <p class="text-xs sm:text-sm text-gray-500">{{ formatDate(transaction.date) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pokrok cílů -->
      <div v-if="financeStore.activeGoals.length > 0" class="card">
        <h3 class="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Pokrok cílů</h3>
        <div class="space-y-3 sm:space-y-4">
          <div
            v-for="goal in financeStore.activeGoals.slice(0, 3)"
            :key="goal.id"
            class="space-y-2"
          >
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
              <span class="text-sm sm:text-base font-medium text-gray-900 truncate">{{ goal.name }}</span>
              <span class="text-xs sm:text-sm text-gray-500 whitespace-nowrap">
                {{ formatCurrency(goal.current_amount) }} / {{ formatCurrency(goal.target_amount) }}
              </span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-1.5 sm:h-2">
              <div
                class="bg-gradient-to-r from-blue-600 to-indigo-600 h-1.5 sm:h-2 rounded-full transition-all duration-300"
                :style="{ width: `${Math.min((goal.current_amount / goal.target_amount) * 100, 100)}%` }"
              ></div>
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
  ArrowUpDown,
  BarChart3,
  PieChart
} from 'lucide-vue-next'
import AddTransactionModal from '@/components/AddTransactionModal.vue'

const authStore = useAuthStore()
const financeStore = useFinanceStore()

const showAddTransactionModal = ref(false)

const currentDate = computed(() => {
  return new Date().toLocaleDateString('cs-CZ', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('cs-CZ', {
    style: 'currency',
    currency: 'CZK'
  }).format(amount || 0)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('cs-CZ')
}

const handleTransactionAdded = () => {
  showAddTransactionModal.value = false
  // Data se automaticky aktualizují díky store
}

onMounted(() => {
  // Data se načtou automaticky v Layout komponentě
})
</script>