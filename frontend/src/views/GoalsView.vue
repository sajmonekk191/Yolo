<template>
  <div class="space-y-6">
    <!-- Nadpis a tlačítko pro přidání -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Finanční cíle</h1>
        <p class="text-gray-600">Sledujte pokrok svých spořicích cílů</p>
      </div>
      <button
        @click="showAddModal = true"
        class="btn-primary flex items-center space-x-2"
      >
        <Plus class="w-5 h-5" />
        <span>Přidat cíl</span>
      </button>
    </div>

    <!-- Statistiky cílů -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Aktivní cíle</p>
            <p class="text-2xl font-bold text-blue-600">{{ financeStore.activeGoals.length }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <Target class="w-6 h-6 text-blue-600" />
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Dokončené cíle</p>
            <p class="text-2xl font-bold text-green-600">{{ financeStore.completedGoals.length }}</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <CheckCircle class="w-6 h-6 text-green-600" />
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Celkový cíl</p>
            <p class="text-2xl font-bold text-purple-600">{{ formatCurrency(totalGoalAmount) }}</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <TrendingUp class="w-6 h-6 text-purple-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Loading stav -->
    <div v-if="financeStore.isGoalsLoading" class="flex items-center justify-center py-12">
      <div class="loading-spinner"></div>
    </div>

    <!-- Prázdný stav -->
    <div v-else-if="financeStore.goals.length === 0" class="card text-center py-12">
      <Target class="w-16 h-16 mx-auto mb-4 text-gray-300" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">Žádné cíle</h3>
      <p class="text-gray-500 mb-4">Nastavte si své první finanční cíle a začněte spořit!</p>
      <button
        @click="showAddModal = true"
        class="btn-primary"
      >
        Vytvořit první cíl
      </button>
    </div>

    <!-- Seznam cílů -->
    <div v-else class="space-y-6">
      <!-- Aktivní cíle -->
      <div v-if="financeStore.activeGoals.length > 0">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Aktivní cíle</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="goal in financeStore.activeGoals"
            :key="goal.id"
            class="card hover:shadow-md transition-shadow"
          >
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="font-semibold text-gray-900">{{ goal.name }}</h3>
                <p class="text-sm text-gray-500">{{ goal.description }}</p>
              </div>
              <div class="flex items-center space-x-1">
                <button
                  @click="editGoal(goal)"
                  class="p-1 text-gray-400 hover:text-blue-600 rounded"
                >
                  <Edit2 class="w-4 h-4" />
                </button>
                <button
                  @click="deleteGoal(goal)"
                  class="p-1 text-gray-400 hover:text-red-600 rounded"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>

            <!-- Pokrok -->
            <div class="mb-4">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-gray-700">Pokrok</span>
                <span class="text-sm text-gray-500">
                  {{ Math.round((goal.current_amount / goal.target_amount) * 100) }}%
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div
                  class="bg-gradient-to-r from-blue-600 to-indigo-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${Math.min((goal.current_amount / goal.target_amount) * 100, 100)}%` }"
                ></div>
              </div>
              <div class="flex items-center justify-between mt-2 text-sm">
                <span class="text-gray-600">{{ formatCurrency(goal.current_amount) }}</span>
                <span class="font-medium text-gray-900">{{ formatCurrency(goal.target_amount) }}</span>
              </div>
            </div>

            <!-- Deadline -->
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center space-x-1 text-gray-500">
                <Calendar class="w-4 h-4" />
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
                class="flex-1 btn-secondary flex items-center justify-center space-x-1 py-2"
              >
                <Plus class="w-4 h-4" />
                <span>Vložit</span>
              </button>
              <button
                v-if="goal.current_amount > 0"
                @click="withdrawFromGoal(goal)"
                class="flex-1 btn-secondary flex items-center justify-center space-x-1 py-2"
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
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Dokončené cíle</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="goal in financeStore.completedGoals"
            :key="goal.id"
            class="card bg-green-50 border-green-200"
          >
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="font-semibold text-gray-900">{{ goal.name }}</h3>
                <p class="text-sm text-gray-500">{{ goal.description }}</p>
              </div>
              <div class="flex items-center space-x-1">
                <CheckCircle class="w-5 h-5 text-green-600" />
                <button
                  @click="deleteGoal(goal)"
                  class="p-1 text-gray-400 hover:text-red-600 rounded"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>

            <div class="mb-4">
              <div class="w-full bg-green-200 rounded-full h-2">
                <div class="bg-green-600 h-2 rounded-full w-full"></div>
              </div>
              <div class="flex items-center justify-between mt-2 text-sm">
                <span class="text-green-700 font-medium">{{ formatCurrency(goal.target_amount) }}</span>
                <span class="text-green-600">100%</span>
              </div>
            </div>

            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center space-x-1 text-gray-500">
                <Calendar class="w-4 h-4" />
                <span>{{ formatDate(goal.target_date) }}</span>
              </div>
              <div class="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
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
    return 'bg-green-100 text-green-800'
  } else if (targetDate < today) {
    return 'bg-red-100 text-red-800'
  } else if (progress >= 75) {
    return 'bg-yellow-100 text-yellow-800'
  } else {
    return 'bg-blue-100 text-blue-800'
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