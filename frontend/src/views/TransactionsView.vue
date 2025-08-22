<template>
  <div class="space-y-6">
    <!-- Nadpis a tlačítko pro přidání -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Transakce</h1>
        <p class="text-gray-600">Správa příjmů a výdajů</p>
      </div>
      <button
        @click="showAddModal = true"
        class="btn-primary flex items-center space-x-2"
      >
        <Plus class="w-5 h-5" />
        <span>Přidat transakci</span>
      </button>
    </div>

    <!-- Filtry a vyhledávání -->
    <div class="card">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <!-- Vyhledávání -->
        <div class="relative">
          <Search class="absolute left-3 top-3 w-5 h-5 text-gray-400" />
          <input
            v-model="filters.search"
            type="text"
            placeholder="Hledat transakce..."
            class="form-input pl-10"
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
          placeholder="Datum od"
        />
      </div>
    </div>

    <!-- Statistiky transakcí -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Celkové příjmy</p>
            <p class="text-2xl font-bold text-green-600">{{ formatCurrency(totalIncome) }}</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <TrendingUp class="w-6 h-6 text-green-600" />
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Celkové výdaje</p>
            <p class="text-2xl font-bold text-red-600">{{ formatCurrency(totalExpenses) }}</p>
          </div>
          <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
            <TrendingDown class="w-6 h-6 text-red-600" />
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Celkový počet</p>
            <p class="text-2xl font-bold text-blue-600">{{ filteredTransactions.length }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <Hash class="w-6 h-6 text-blue-600" />
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
      <div v-else-if="filteredTransactions.length === 0" class="text-center py-12">
        <ArrowUpDown class="w-16 h-16 mx-auto mb-4 text-gray-300" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">Žádné transakce</h3>
        <p class="text-gray-500 mb-4">
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

      <!-- Tabulka transakcí -->
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-3 px-4 font-medium text-gray-900">Datum</th>
              <th class="text-left py-3 px-4 font-medium text-gray-900">Popis</th>
              <th class="text-left py-3 px-4 font-medium text-gray-900">Kategorie</th>
              <th class="text-left py-3 px-4 font-medium text-gray-900">Částka</th>
              <th class="text-left py-3 px-4 font-medium text-gray-900">Akce</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="transaction in paginatedTransactions"
              :key="transaction.id"
              class="border-b border-gray-100 hover:bg-gray-50"
            >
              <td class="py-3 px-4 text-sm text-gray-600">
                {{ formatDate(transaction.date) }}
              </td>
              <td class="py-3 px-4">
                <div class="flex items-center space-x-3">
                  <div
                    class="w-8 h-8 rounded-lg flex items-center justify-center"
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
                  <span class="font-medium text-gray-900">{{ transaction.description }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-sm text-gray-600">
                {{ getCategoryName(transaction.category_id) }}
              </td>
              <td class="py-3 px-4">
                <span
                  class="font-semibold"
                  :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'"
                >
                  {{ transaction.type === 'income' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
                </span>
              </td>
              <td class="py-3 px-4">
                <div class="flex items-center space-x-2">
                  <button
                    @click="editTransaction(transaction)"
                    class="p-1 text-gray-400 hover:text-blue-600 rounded"
                  >
                    <Edit2 class="w-4 h-4" />
                  </button>
                  <button
                    @click="deleteTransaction(transaction)"
                    class="p-1 text-gray-400 hover:text-red-600 rounded"
                  >
                    <Trash2 class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Paginace -->
      <div v-if="totalPages > 1" class="flex items-center justify-between mt-6 pt-6 border-t border-gray-200">
        <div class="text-sm text-gray-600">
          Zobrazeno {{ ((currentPage - 1) * pageSize) + 1 }} - {{ Math.min(currentPage * pageSize, filteredTransactions.length) }} z {{ filteredTransactions.length }} transakcí
        </div>
        <div class="flex items-center space-x-2">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="btn-secondary px-3 py-1 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Předchozí
          </button>
          <span class="text-sm text-gray-600">
            {{ currentPage }} z {{ totalPages }}
          </span>
          <button
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="btn-secondary px-3 py-1 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
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

const filters = reactive({
  search: '',
  type: '',
  category: '',
  dateFrom: ''
})

const filteredTransactions = computed(() => {
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

  // Řazení podle data (nejnovější první)
  return transactions.sort((a, b) => new Date(b.date) - new Date(a.date))
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

const getCategoryName = (categoryId) => {
  const category = financeStore.categories.find(c => c.id === categoryId)
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