<template>
  <div class="space-y-6">
    <!-- Nadpis a tlačítko pro přidání -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-gray-900">Transakce</h1>
        <p class="text-sm sm:text-base text-gray-600">Správa příjmů a výdajů</p>
      </div>
      <button
        @click="showAddModal = true"
        class="btn-primary flex items-center justify-center space-x-2 w-full sm:w-auto"
      >
        <Plus class="w-4 h-4 sm:w-5 sm:h-5" />
        <span class="text-sm sm:text-base">Přidat transakci</span>
      </button>
    </div>

    <!-- Filtry a vyhledávání -->
    <div class="card">
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
        <!-- Vyhledávání -->
        <div class="relative sm:col-span-2 md:col-span-1">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 sm:w-5 sm:h-5 text-gray-400" />
          <input
            v-model="filters.search"
            type="text"
            placeholder="Hledat transakce..."
            class="form-input pl-9 sm:pl-10"
          />
        </div>

        <!-- Typ transakce -->
        <select v-model="filters.type" class="form-input">
          <option value="">Všechny typy</option>
          <option value="income">Příjmy</option>
          <option value="expense">Výdaje</option>
        </select>

        <!-- Kategorie -->
        <select v-model="filters.category" class="form-input">
          <option value="">Všechny kategorie</option>
          <option
            v-for="category in financeStore.categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>

        <!-- Datum od -->
        <input
          v-model="filters.dateFrom"
          type="date"
          class="form-input"
          placeholder="dd.mm.yyyy"
        />
      </div>
    </div>

    <!-- Statistiky transakcí -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
      <div class="card">
        <div class="flex items-center justify-between">
          <div class="flex-1 min-w-0">
            <p class="text-xs sm:text-sm text-gray-600 font-medium">Celkové příjmy</p>
            <p class="text-lg sm:text-xl md:text-2xl font-bold text-green-600 truncate">{{ formatCurrency(totalIncome) }}</p>
          </div>
          <div class="w-10 h-10 sm:w-12 sm:h-12 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0 ml-3">
            <TrendingUp class="w-5 h-5 sm:w-6 sm:h-6 text-green-600" />
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div class="flex-1 min-w-0">
            <p class="text-xs sm:text-sm text-gray-600 font-medium">Celkové výdaje</p>
            <p class="text-lg sm:text-xl md:text-2xl font-bold text-red-600 truncate">{{ formatCurrency(totalExpenses) }}</p>
          </div>
          <div class="w-10 h-10 sm:w-12 sm:h-12 bg-red-100 rounded-lg flex items-center justify-center flex-shrink-0 ml-3">
            <TrendingDown class="w-5 h-5 sm:w-6 sm:h-6 text-red-600" />
          </div>
        </div>
      </div>

      <div class="card sm:col-span-2 md:col-span-1">
        <div class="flex items-center justify-between">
          <div class="flex-1 min-w-0">
            <p class="text-xs sm:text-sm text-gray-600 font-medium">Celkový počet</p>
            <p class="text-lg sm:text-xl md:text-2xl font-bold text-blue-600">{{ filteredTransactions.length }}</p>
          </div>
          <div class="w-10 h-10 sm:w-12 sm:h-12 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0 ml-3">
            <Hash class="w-5 h-5 sm:w-6 sm:h-6 text-blue-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Seznam transakcí -->
    <div class="card">
      <!-- Loading stav -->
      <div v-if="financeStore.isTransactionsLoading" class="flex items-center justify-center py-12">
        <div class="loading-spinner"></div>
      </div>

      <!-- Prázdný stav -->
      <div v-else-if="filteredTransactions.length === 0" class="text-center py-8 sm:py-12">
        <ArrowUpDown class="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-3 sm:mb-4 text-gray-300" />
        <h3 class="text-base sm:text-lg font-medium text-gray-900 mb-2">Žádné transakce</h3>
        <p class="text-sm sm:text-base text-gray-500 mb-4 px-4">
          {{ filters.search || filters.type || filters.category ? 'Žádné transakce nevyhovují zadaným filtrům.' : 'Zatím nemáte žádné transakce.' }}
        </p>
        <button
          v-if="!filters.search && !filters.type && !filters.category"
          @click="showAddModal = true"
          class="btn-primary"
        >
          Přidat první transakci
        </button>
      </div>

      <!-- Mobilní zobrazení transakcí -->
      <div v-else-if="isMobile" class="space-y-3">
        <div
          v-for="transaction in paginatedTransactions"
          :key="transaction.id"
          class="border rounded-lg p-3 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between mb-2">
            <div class="flex items-center space-x-2">
              <div
                class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                :class="transaction.type === 'income' ? 'bg-green-100' : 'bg-red-100'"
              >
                <TrendingUp
                  v-if="transaction.type === 'income'"
                  class="w-4 h-4 text-green-600"
                />
                <TrendingDown
                  v-else
                  class="w-4 h-4 text-red-600"
                />
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-900 text-sm truncate">{{ transaction.description }}</p>
                <p class="text-xs text-gray-500">{{ getCategoryName(transaction) }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <button
                @click="editTransaction(transaction)"
                class="p-1.5 text-gray-400 hover:text-blue-600 rounded"
              >
                <Edit2 class="w-4 h-4" />
              </button>
              <button
                @click="deleteTransaction(transaction)"
                class="p-1.5 text-gray-400 hover:text-red-600 rounded"
              >
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-xs text-gray-500">{{ formatDate(transaction.date) }}</span>
            <span
              class="font-semibold text-sm"
              :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'"
            >
              {{ transaction.type === 'income' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Desktop tabulka transakcí -->
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-3 px-3 sm:px-4 text-xs sm:text-sm font-medium text-gray-900">Datum</th>
              <th class="text-left py-3 px-3 sm:px-4 text-xs sm:text-sm font-medium text-gray-900">Popis</th>
              <th class="text-left py-3 px-3 sm:px-4 text-xs sm:text-sm font-medium text-gray-900 hidden sm:table-cell">Kategorie</th>
              <th class="text-left py-3 px-3 sm:px-4 text-xs sm:text-sm font-medium text-gray-900">Částka</th>
              <th class="text-left py-3 px-3 sm:px-4 text-xs sm:text-sm font-medium text-gray-900">Akce</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="transaction in paginatedTransactions"
              :key="transaction.id"
              class="border-b border-gray-100 hover:bg-gray-50"
            >
              <td class="py-2 sm:py-3 px-3 sm:px-4 text-xs sm:text-sm text-gray-600">
                {{ formatDate(transaction.date) }}
              </td>
              <td class="py-2 sm:py-3 px-3 sm:px-4">
                <div class="flex items-center space-x-2 sm:space-x-3">
                  <div
                    class="w-6 h-6 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                    :class="transaction.type === 'income' ? 'bg-green-100' : 'bg-red-100'"
                  >
                    <TrendingUp
                      v-if="transaction.type === 'income'"
                      class="w-3 h-3 sm:w-4 sm:h-4 text-green-600"
                    />
                    <TrendingDown
                      v-else
                      class="w-3 h-3 sm:w-4 sm:h-4 text-red-600"
                    />
                  </div>
                  <span class="text-xs sm:text-sm font-medium text-gray-900 truncate max-w-[150px] sm:max-w-none">{{ transaction.description }}</span>
                </div>
              </td>
              <td class="py-2 sm:py-3 px-3 sm:px-4 text-xs sm:text-sm text-gray-600 hidden sm:table-cell">
                {{ getCategoryName(transaction) }}
              </td>
              <td class="py-2 sm:py-3 px-3 sm:px-4">
                <span
                  class="text-xs sm:text-sm font-semibold"
                  :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'"
                >
                  {{ transaction.type === 'income' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
                </span>
              </td>
              <td class="py-2 sm:py-3 px-3 sm:px-4">
                <div class="flex items-center space-x-1 sm:space-x-2">
                  <button
                    @click="editTransaction(transaction)"
                    class="p-1 text-gray-400 hover:text-blue-600 rounded"
                  >
                    <Edit2 class="w-3 h-3 sm:w-4 sm:h-4" />
                  </button>
                  <button
                    @click="deleteTransaction(transaction)"
                    class="p-1 text-gray-400 hover:text-red-600 rounded"
                  >
                    <Trash2 class="w-3 h-3 sm:w-4 sm:h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Paginace -->
      <div v-if="totalPages > 1" class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mt-4 sm:mt-6 pt-4 sm:pt-6 border-t border-gray-200">
        <div class="text-xs sm:text-sm text-gray-600 text-center sm:text-left">
          Zobrazeno {{ ((currentPage - 1) * pageSize) + 1 }} - {{ Math.min(currentPage * pageSize, filteredTransactions.length) }} z {{ filteredTransactions.length }}
        </div>
        <div class="flex items-center justify-center space-x-2">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="btn-secondary px-2 sm:px-3 py-1 text-xs sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Předchozí
          </button>
          <span class="text-xs sm:text-sm text-gray-600 px-2">
            {{ currentPage }} z {{ totalPages }}
          </span>
          <button
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="btn-secondary px-2 sm:px-3 py-1 text-xs sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Další
          </button>
        </div>
      </div>
    </div>

    <!-- Modály -->
    <AddTransactionModal
      v-if="showAddModal"
      @close="showAddModal = false"
      @transaction-added="handleTransactionAdded"
    />

    <EditTransactionModal
      v-if="showEditModal && selectedTransaction"
      :transaction="selectedTransaction"
      @close="closeEditModal"
      @transaction-updated="handleTransactionUpdated"
    />

    <DeleteConfirmModal
      v-if="showDeleteModal && selectedTransaction"
      :title="`Smazat transakci &quot;${selectedTransaction.description}&quot;?`"
      :message="'Tato akce je nevratná. Transakce bude trvale odstraněna.'"
      @close="closeDeleteModal"
      @confirm="handleDeleteConfirm"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import {
  Plus,
  Search,
  TrendingUp,
  TrendingDown,
  ArrowUpDown,
  Hash,
  Edit2,
  Trash2
} from 'lucide-vue-next'
import AddTransactionModal from '@/components/AddTransactionModal.vue'
import EditTransactionModal from '@/components/EditTransactionModal.vue'
import DeleteConfirmModal from '@/components/DeleteConfirmModal.vue'

const financeStore = useFinanceStore()

const showAddModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const selectedTransaction = ref(null)
const currentPage = ref(1)
const pageSize = 20
const isMobile = ref(window.innerWidth < 640)

// Sledování změny velikosti okna
onMounted(() => {
  const handleResize = () => {
    isMobile.value = window.innerWidth < 640
  }
  window.addEventListener('resize', handleResize)
  return () => window.removeEventListener('resize', handleResize)
})

const filters = reactive({
  search: '',
  type: '',
  category: '',
  dateFrom: ''
})

const filteredTransactions = computed(() => {
  // Transakce jsou již seřazené ze store (nejnovější první)
  let transactions = [...financeStore.transactions]

  // Filtrování podle vyhledávání
  if (filters.search) {
    const search = filters.search.toLowerCase()
    transactions = transactions.filter(t =>
      t.description.toLowerCase().includes(search)
    )
  }

  // Filtrování podle typu
  if (filters.type) {
    transactions = transactions.filter(t => t.type === filters.type)
  }

  // Filtrování podle kategorie
  if (filters.category) {
    transactions = transactions.filter(t => t.category_id === parseInt(filters.category))
  }

  // Filtrování podle data
  if (filters.dateFrom) {
    transactions = transactions.filter(t => t.date >= filters.dateFrom)
  }

  // Transakce jsou již seřazené ze store, není potřeba znovu řadit
  return transactions
})

const totalPages = computed(() => {
  return Math.ceil(filteredTransactions.value.length / pageSize)
})

const paginatedTransactions = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredTransactions.value.slice(start, end)
})

const totalIncome = computed(() => {
  return filteredTransactions.value
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0)
})

const totalExpenses = computed(() => {
  return filteredTransactions.value
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0)
})

const getCategoryName = (transaction) => {
  // Pokud transakce má přímo informaci o kategorii, použij ji
  if (transaction.category && transaction.category.name) {
    return transaction.category.name
  }
  // Jinak zkus najít v seznamu kategorií
  const category = financeStore.categories.find(c => c.id === transaction.category_id)
  return category ? category.name : 'Neznámá kategorie'
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('cs-CZ', {
    style: 'currency',
    currency: 'CZK'
  }).format(amount || 0)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('cs-CZ')
}

const editTransaction = (transaction) => {
  selectedTransaction.value = transaction
  showEditModal.value = true
}

const deleteTransaction = (transaction) => {
  selectedTransaction.value = transaction
  showDeleteModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  selectedTransaction.value = null
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  selectedTransaction.value = null
}

const handleTransactionAdded = () => {
  showAddModal.value = false
}

const handleTransactionUpdated = () => {
  closeEditModal()
}

const handleDeleteConfirm = async () => {
  if (selectedTransaction.value) {
    await financeStore.deleteTransaction(selectedTransaction.value.id)
    closeDeleteModal()
  }
}

// Reset stránkování při změně filtrů
watch(() => [filters.search, filters.type, filters.category, filters.dateFrom], () => {
  currentPage.value = 1
})

onMounted(() => {
  // Data se načtou automaticky v Layout komponentě
})
</script>