<template>
  <div class="space-y-6">
    <!-- Nadpis a tlačítko pro přidání -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white transition-all duration-300">Rozpočty</h1>
        <p class="text-gray-600 dark:text-gray-400 transition-all duration-300">Spravujte své měsíční rozpočty podle kategorií</p>
      </div>
      <button
        @click="showAddModal = true"
        class="btn-primary flex items-center space-x-2 transition-all duration-300"
      >
        <Plus class="w-5 h-5" />
        <span>Přidat rozpočet</span>
      </button>
    </div>

    <!-- Celkový přehled rozpočtu -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="card dark:bg-gray-800 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm font-medium transition-all duration-300">Celkový rozpočet</p>
            <p class="text-2xl font-bold text-blue-600 dark:text-blue-400 transition-all duration-300">{{ formatCurrency(totalBudget) }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center transition-all duration-300">
            <PiggyBank class="w-6 h-6 text-blue-600 dark:text-blue-400" />
          </div>
        </div>
      </div>

      <div class="card dark:bg-gray-800 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm font-medium transition-all duration-300">Utraceno</p>
            <p class="text-2xl font-bold text-red-600 dark:text-red-400 transition-all duration-300">{{ formatCurrency(totalSpent) }}</p>
          </div>
          <div class="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center justify-center transition-all duration-300">
            <TrendingDown class="w-6 h-6 text-red-600 dark:text-red-400" />
          </div>
        </div>
      </div>

      <div class="card dark:bg-gray-800 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm font-medium transition-all duration-300">Zbývá</p>
            <p 
              class="text-2xl font-bold transition-all duration-300"
              :class="totalRemaining >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
            >
              {{ formatCurrency(totalRemaining) }}
            </p>
          </div>
          <div 
            class="w-12 h-12 rounded-lg flex items-center justify-center transition-all duration-300"
            :class="totalRemaining >= 0 ? 'bg-green-100 dark:bg-green-900/30' : 'bg-red-100 dark:bg-red-900/30'"
          >
            <Wallet 
              class="w-6 h-6" 
              :class="totalRemaining >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
            />
          </div>
        </div>
      </div>

      <div class="card dark:bg-gray-800 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm font-medium transition-all duration-300">Aktivní rozpočty</p>
            <p class="text-2xl font-bold text-purple-600 dark:text-purple-400 transition-all duration-300">{{ financeStore.activeBudgets.length }}</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center transition-all duration-300">
            <BarChart3 class="w-6 h-6 text-purple-600 dark:text-purple-400" />
          </div>
        </div>
      </div>
    </div>

    <!-- Celkový pokrok -->
    <div class="card dark:bg-gray-800 transition-all duration-300">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 transition-all duration-300">Celkový pokrok rozpočtu</h3>
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300 transition-all duration-300">Využití rozpočtu</span>
          <span class="text-sm text-gray-500 dark:text-gray-400 transition-all duration-300">
            {{ totalBudget > 0 ? Math.round((totalSpent / totalBudget) * 100) : 0 }}%
          </span>
        </div>
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 transition-all duration-300">
          <div
            class="h-3 rounded-full transition-all duration-300"
            :class="getBudgetProgressClass(totalSpent, totalBudget)"
            :style="{ width: `${Math.min((totalSpent / totalBudget) * 100, 100)}%` }"
          ></div>
        </div>
        <div class="flex items-center justify-between text-sm">
          <span class="text-gray-600 dark:text-gray-400 transition-all duration-300">{{ formatCurrency(totalSpent) }}</span>
          <span class="font-medium text-gray-900 dark:text-white transition-all duration-300">{{ formatCurrency(totalBudget) }}</span>
        </div>
      </div>
    </div>

    <!-- Loading stav -->
    <div v-if="financeStore.isBudgetsLoading" class="flex items-center justify-center py-12">
      <div class="loading-spinner"></div>
    </div>

    <!-- Prázdný stav -->
    <div v-else-if="financeStore.budgets.length === 0" class="card dark:bg-gray-800 text-center py-12 transition-all duration-300">
      <PiggyBank class="w-16 h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600 transition-all duration-300" />
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2 transition-all duration-300">Žádné rozpočty</h3>
      <p class="text-gray-500 dark:text-gray-400 mb-4 transition-all duration-300">Vytvořte své první rozpočty a začněte spravovat výdaje!</p>
      <button
        @click="showAddModal = true"
        class="btn-primary transition-all duration-300"
      >
        Vytvořit první rozpočet
      </button>
    </div>

    <!-- Seznam rozpočtů -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div
        v-for="budget in financeStore.budgets"
        :key="budget.id"
        class="card dark:bg-gray-800 hover:shadow-md dark:hover:shadow-2xl transition-all duration-300"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-start space-x-3">
            <div class="flex-shrink-0 mt-1">
              <CategoryIcon
                v-if="getCategory(budget.category_id)"
                :icon="getCategory(budget.category_id).icon"
                :color="getCategory(budget.category_id).color"
              />
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 dark:text-white transition-all duration-300">{{ getCategoryName(budget.category_id) }}</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400 transition-all duration-300">{{ getMonthName(budget.month) }} {{ budget.year }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-1">
            <div
              class="px-2 py-1 rounded-full text-xs font-medium transition-all duration-300"
              :class="budget.is_active ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400' : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300'"
            >
              {{ budget.is_active ? 'Aktivní' : 'Neaktivní' }}
            </div>
            <button
              @click="editBudget(budget)"
              class="p-1 text-gray-400 dark:text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 rounded transition-all duration-300"
            >
              <Edit2 class="w-4 h-4" />
            </button>
            <button
              @click="deleteBudget(budget)"
              class="p-1 text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 rounded transition-all duration-300"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Pokrok rozpočtu -->
        <div class="mb-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300 transition-all duration-300">Pokrok</span>
            <span class="text-sm text-gray-500 dark:text-gray-400 transition-all duration-300">
              {{ Math.round((getBudgetSpent(budget) / budget.amount) * 100) }}%
            </span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 transition-all duration-300">
            <div
              class="h-2 rounded-full transition-all duration-300"
              :class="getBudgetProgressClass(getBudgetSpent(budget), budget.amount)"
              :style="{ width: `${Math.min((getBudgetSpent(budget) / budget.amount) * 100, 100)}%` }"
            ></div>
          </div>
          <div class="flex items-center justify-between mt-2 text-sm">
            <span class="text-gray-600 dark:text-gray-400 transition-all duration-300">{{ formatCurrency(getBudgetSpent(budget)) }}</span>
            <span class="font-medium text-gray-900 dark:text-white transition-all duration-300">{{ formatCurrency(budget.amount) }}</span>
          </div>
        </div>

        <!-- Zbývající částka -->
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-gray-400 transition-all duration-300">Zbývá:</span>
          <span 
            class="text-sm font-medium transition-all duration-300"
            :class="getBudgetRemaining(budget) >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
          >
            {{ formatCurrency(getBudgetRemaining(budget)) }}
          </span>
        </div>

        <!-- Varování při překročení -->
        <div 
          v-if="getBudgetSpent(budget) > budget.amount" 
          class="mt-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg p-3 transition-all duration-300"
        >
          <div class="flex items-center">
            <AlertTriangle class="w-4 h-4 text-red-500 dark:text-red-400 mr-2" />
            <span class="text-sm text-red-700 dark:text-red-400 font-medium transition-all duration-300">Rozpočet překročen!</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Modály -->
    <AddBudgetModal
      v-if="showAddModal"
      @close="showAddModal = false"
      @budget-added="handleBudgetAdded"
    />

    <EditBudgetModal
      v-if="showEditModal && selectedBudget"
      :budget="selectedBudget"
      @close="closeEditModal"
      @budget-updated="handleBudgetUpdated"
    />

    <DeleteConfirmModal
      v-if="showDeleteModal && selectedBudget"
      :title="`Smazat rozpočet pro &quot;${getCategoryName(selectedBudget.category_id)}&quot;?`"
      :message="'Tato akce je nevratná. Rozpočet bude trvale odstraněn.'"
      @close="closeDeleteModal"
      @confirm="handleDeleteConfirm"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import {
  Plus,
  PiggyBank,
  TrendingDown,
  Wallet,
  BarChart3,
  Edit2,
  Trash2,
  AlertTriangle
} from 'lucide-vue-next'
import AddBudgetModal from '@/components/AddBudgetModal.vue'
import EditBudgetModal from '@/components/EditBudgetModal.vue'
import DeleteConfirmModal from '@/components/DeleteConfirmModal.vue'
import CategoryIcon from '@/components/CategoryIcon.vue'

const financeStore = useFinanceStore()

const showAddModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const selectedBudget = ref(null)

const totalBudget = computed(() => {
  return financeStore.activeBudgets.reduce((sum, budget) => sum + budget.amount, 0)
})

const totalSpent = computed(() => {
  return financeStore.activeBudgets.reduce((sum, budget) => sum + getBudgetSpent(budget), 0)
})

const totalRemaining = computed(() => {
  return totalBudget.value - totalSpent.value
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('cs-CZ', {
    style: 'currency',
    currency: 'CZK'
  }).format(amount || 0)
}

const getCategoryName = (categoryId) => {
  const category = financeStore.categories.find(c => c.id === categoryId)
  return category ? category.name : 'Neznámá kategorie'
}

const getCategory = (categoryId) => {
  return financeStore.categories.find(c => c.id === categoryId)
}

const getMonthName = (month) => {
  const months = [
    'Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen',
    'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec'
  ]
  return months[month - 1] || 'Neznámý měsíc'
}

const getBudgetSpent = (budget) => {
  // Použij hodnotu spent z databáze (backend již vypočítává správnou hodnotu)
  return budget.spent || 0
}

const getBudgetRemaining = (budget) => {
  return budget.amount - getBudgetSpent(budget)
}

const getBudgetProgressClass = (spent, budget) => {
  const percentage = (spent / budget) * 100
  if (percentage >= 100) {
    return 'bg-red-500'
  } else if (percentage >= 80) {
    return 'bg-yellow-500'
  } else {
    return 'bg-green-500'
  }
}

const editBudget = (budget) => {
  selectedBudget.value = budget
  showEditModal.value = true
}

const deleteBudget = (budget) => {
  selectedBudget.value = budget
  showDeleteModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  selectedBudget.value = null
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  selectedBudget.value = null
}

const handleBudgetAdded = () => {
  showAddModal.value = false
}

const handleBudgetUpdated = () => {
  closeEditModal()
}

const handleDeleteConfirm = async () => {
  if (selectedBudget.value) {
    await financeStore.deleteBudget(selectedBudget.value.id)
    closeDeleteModal()
  }
}

onMounted(() => {
  // Data se načtou automaticky v Layout komponentě
})
</script>