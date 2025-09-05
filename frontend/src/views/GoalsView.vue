<template>
  <div class="space-y-6 transition-all duration-300">
    <!-- Nadpis a tlačítko pro přidání -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white transition-all duration-300">Finanční cíle</h1>
        <p class="text-gray-600 dark:text-gray-400 transition-all duration-300">Sledujte pokrok svých spořicích cílů</p>
      </div>
      <button
        @click="showAddModal = true"
        class="btn-primary flex items-center space-x-2 transition-all duration-300"
      >
        <Plus class="w-5 h-5" />
        <span>Přidat cíl</span>
      </button>
    </div>

    <!-- Statistiky cílů -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card dark:bg-gray-800 dark:border-gray-700 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm font-medium transition-all duration-300">Aktivní cíle</p>
            <p class="text-2xl font-bold text-blue-600 dark:text-blue-400 transition-all duration-300">{{ financeStore.activeGoals.length }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center transition-all duration-300">
            <Target class="w-6 h-6 text-blue-600 dark:text-blue-400 transition-all duration-300" />
          </div>
        </div>
      </div>

      <div class="card dark:bg-gray-800 dark:border-gray-700 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm font-medium transition-all duration-300">Dokončené cíle</p>
            <p class="text-2xl font-bold text-green-600 dark:text-green-400 transition-all duration-300">{{ financeStore.completedGoals.length }}</p>
          </div>
          <div class="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center transition-all duration-300">
            <CheckCircle class="w-6 h-6 text-green-600 dark:text-green-400 transition-all duration-300" />
          </div>
        </div>
      </div>

      <div class="card dark:bg-gray-800 dark:border-gray-700 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm font-medium transition-all duration-300">Celkový cíl</p>
            <p class="text-2xl font-bold text-purple-600 dark:text-purple-400 transition-all duration-300">{{ formatCurrency(totalGoalAmount) }}</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center transition-all duration-300">
            <TrendingUp class="w-6 h-6 text-purple-600 dark:text-purple-400 transition-all duration-300" />
          </div>
        </div>
      </div>
    </div>

    <!-- Loading stav -->
    <div v-if="financeStore.isGoalsLoading" class="flex items-center justify-center py-12">
      <div class="loading-spinner"></div>
    </div>

    <!-- Prázdný stav -->
    <div v-else-if="financeStore.goals.length === 0" class="card dark:bg-gray-800 dark:border-gray-700 text-center py-12 transition-all duration-300">
      <Target class="w-16 h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600 transition-all duration-300" />
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2 transition-all duration-300">Žádné cíle</h3>
      <p class="text-gray-500 dark:text-gray-400 mb-4 transition-all duration-300">Nastavte si své první finanční cíle a začněte spořit!</p>
      <button
        @click="showAddModal = true"
        class="btn-primary transition-all duration-300"
      >
        Vytvořit první cíl
      </button>
    </div>

    <!-- Seznam cílů -->
    <div v-else class="space-y-6">
      <!-- Aktivní cíle -->
      <div v-if="financeStore.activeGoals.length > 0">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 transition-all duration-300">Aktivní cíle</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="goal in financeStore.activeGoals"
            :key="goal.id"
            class="card dark:bg-gray-800 dark:border-gray-700 hover:shadow-md dark:hover:shadow-2xl transition-all duration-300"
          >
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white transition-all duration-300">{{ goal.name }}</h3>
                <p class="text-sm text-gray-500 dark:text-gray-400 transition-all duration-300">{{ goal.description }}</p>
              </div>
              <div class="flex items-center space-x-1">
                <button
                  @click="editGoal(goal)"
                  class="p-1 text-gray-400 dark:text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 rounded transition-all duration-300"
                >
                  <Edit2 class="w-4 h-4" />
                </button>
                <button
                  @click="deleteGoal(goal)"
                  class="p-1 text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 rounded transition-all duration-300"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>

            <!-- Pokrok -->
            <div class="mb-4">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300 transition-all duration-300">Pokrok</span>
                <span class="text-sm text-gray-500 dark:text-gray-400 transition-all duration-300">
                  {{ Math.round((goal.current_amount / goal.target_amount) * 100) }}%
                </span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 transition-all duration-300">
                <div
                  class="bg-gradient-to-r from-blue-600 to-indigo-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${Math.min((goal.current_amount / goal.target_amount) * 100, 100)}%` }"
                ></div>
              </div>
              <div class="flex items-center justify-between mt-2 text-sm">
                <span class="text-gray-600 dark:text-gray-400 transition-all duration-300">{{ formatCurrency(goal.current_amount) }}</span>
                <span class="font-medium text-gray-900 dark:text-white transition-all duration-300">{{ formatCurrency(goal.target_amount) }}</span>
              </div>
            </div>

            <!-- Deadline -->
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center space-x-1 text-gray-500 dark:text-gray-400 transition-all duration-300">
                <Calendar class="w-4 h-4 transition-all duration-300" />
                <span>{{ formatDate(goal.target_date) }}</span>
              </div>
              <div
                class="px-2 py-1 rounded-full text-xs font-medium"
                :class="getGoalStatusClass(goal)"
              >
                {{ getGoalStatusText(goal) }}
              </div>
            </div>

            <!-- Tlačítka pro přidání/výběr částky -->
            <div class="flex gap-2 mt-4">
              <button
                @click="addToGoal(goal)"
                class="flex-1 btn-secondary flex items-center justify-center space-x-1 py-2 transition-all duration-300"
              >
                <Plus class="w-4 h-4" />
                <span>Vložit</span>
              </button>
              <button
                v-if="goal.current_amount > 0"
                @click="withdrawFromGoal(goal)"
                class="flex-1 btn-secondary flex items-center justify-center space-x-1 py-2 transition-all duration-300"
              >
                <Minus class="w-4 h-4" />
                <span>Vybrat</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Dokončené cíle -->
      <div v-if="financeStore.completedGoals.length > 0">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 transition-all duration-300">Dokončené cíle</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="goal in financeStore.completedGoals"
            :key="goal.id"
            class="card bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800 transition-all duration-300"
          >
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white transition-all duration-300">{{ goal.name }}</h3>
                <p class="text-sm text-gray-500 dark:text-gray-400 transition-all duration-300">{{ goal.description }}</p>
              </div>
              <div class="flex items-center space-x-1">
                <CheckCircle class="w-5 h-5 text-green-600 dark:text-green-400 transition-all duration-300" />
                <button
                  @click="deleteGoal(goal)"
                  class="p-1 text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 rounded transition-all duration-300"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>

            <div class="mb-4">
              <div class="w-full bg-green-200 dark:bg-green-800 rounded-full h-2 transition-all duration-300">
                <div class="bg-green-600 dark:bg-green-500 h-2 rounded-full w-full transition-all duration-300"></div>
              </div>
              <div class="flex items-center justify-between mt-2 text-sm">
                <span class="text-green-700 dark:text-green-400 font-medium transition-all duration-300">{{ formatCurrency(goal.target_amount) }}</span>
                <span class="text-green-600 dark:text-green-400 transition-all duration-300">100%</span>
              </div>
            </div>

            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center space-x-1 text-gray-500 dark:text-gray-400 transition-all duration-300">
                <Calendar class="w-4 h-4 transition-all duration-300" />
                <span>{{ formatDate(goal.target_date) }}</span>
              </div>
              <div class="px-2 py-1 rounded-full text-xs font-medium bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300 transition-all duration-300">
                Dokončeno
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modály -->
    <AddGoalModal
      v-if="showAddModal"
      @close="showAddModal = false"
      @goal-added="handleGoalAdded"
    />

    <EditGoalModal
      v-if="showEditModal && selectedGoal"
      :goal="selectedGoal"
      @close="closeEditModal"
      @goal-updated="handleGoalUpdated"
    />

    <AddToGoalModal
      v-if="showAddToGoalModal && selectedGoal"
      :goal="selectedGoal"
      @close="closeAddToGoalModal"
      @amount-added="handleAmountAdded"
    />

    <DeleteConfirmModal
      v-if="showDeleteModal && selectedGoal"
      :title="`Smazat cíl &quot;${selectedGoal.name}&quot;?`"
      :message="'Tato akce je nevratná. Cíl a veškerý pokrok bude trvale odstraněn.'"
      @close="closeDeleteModal"
      @confirm="handleDeleteConfirm"
    />

    <WithdrawFromGoalModal
      v-if="showWithdrawModal && selectedGoal"
      :goal="selectedGoal"
      @close="closeWithdrawModal"
      @withdrawn="handleWithdrawn"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import {
  Plus,
  Minus,
  Target,
  CheckCircle,
  TrendingUp,
  Edit2,
  Trash2,
  Calendar
} from 'lucide-vue-next'
import AddGoalModal from '@/components/AddGoalModal.vue'
import EditGoalModal from '@/components/EditGoalModal.vue'
import AddToGoalModal from '@/components/AddToGoalModal.vue'
import DeleteConfirmModal from '@/components/DeleteConfirmModal.vue'
import WithdrawFromGoalModal from '@/components/WithdrawFromGoalModal.vue'

const financeStore = useFinanceStore()

const showAddModal = ref(false)
const showEditModal = ref(false)
const showAddToGoalModal = ref(false)
const showDeleteModal = ref(false)
const showWithdrawModal = ref(false)
const selectedGoal = ref(null)

const totalGoalAmount = computed(() => {
  return financeStore.goals.reduce((sum, goal) => sum + goal.target_amount, 0)
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

const getGoalStatusClass = (goal) => {
  const today = new Date()
  const targetDate = new Date(goal.target_date)
  const progress = (goal.current_amount / goal.target_amount) * 100

  if (progress >= 100) {
    return 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300 transition-all duration-300'
  } else if (targetDate < today) {
    return 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300 transition-all duration-300'
  } else if (progress >= 75) {
    return 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-300 transition-all duration-300'
  } else {
    return 'bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-300 transition-all duration-300'
  }
}

const getGoalStatusText = (goal) => {
  const today = new Date()
  const targetDate = new Date(goal.target_date)
  const progress = (goal.current_amount / goal.target_amount) * 100

  if (progress >= 100) {
    return 'Dokončeno'
  } else if (targetDate < today) {
    return 'Prošlé'
  } else if (progress >= 75) {
    return 'Blízko cíle'
  } else {
    return 'V procesu'
  }
}

const editGoal = (goal) => {
  selectedGoal.value = goal
  showEditModal.value = true
}

const deleteGoal = (goal) => {
  selectedGoal.value = goal
  showDeleteModal.value = true
}

const addToGoal = (goal) => {
  selectedGoal.value = goal
  showAddToGoalModal.value = true
}

const withdrawFromGoal = (goal) => {
  selectedGoal.value = goal
  showWithdrawModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  selectedGoal.value = null
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  selectedGoal.value = null
}

const closeAddToGoalModal = () => {
  showAddToGoalModal.value = false
  selectedGoal.value = null
}

const closeWithdrawModal = () => {
  showWithdrawModal.value = false
  selectedGoal.value = null
}

const handleGoalAdded = () => {
  showAddModal.value = false
}

const handleGoalUpdated = () => {
  closeEditModal()
}

const handleAmountAdded = () => {
  closeAddToGoalModal()
}

const handleWithdrawn = () => {
  closeWithdrawModal()
}

const handleDeleteConfirm = async () => {
  if (selectedGoal.value) {
    await financeStore.deleteGoal(selectedGoal.value.id)
    closeDeleteModal()
  }
}

onMounted(() => {
  // Data se načtou automaticky v Layout komponentě
})
</script>