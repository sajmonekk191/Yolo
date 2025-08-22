<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Pozadí overlay -->
      <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" @click="$emit('close')"></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-md p-6 my-8 text-left align-middle transition-all transform bg-white shadow-xl rounded-xl">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Přidat k cíli</h3>
          <button @click="$emit('close')" class="p-2 text-gray-400 hover:text-gray-600 rounded-lg">
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Informace o cíli -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h4 class="font-medium text-blue-900 mb-2">{{ goal.name }}</h4>
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-blue-700">Aktuální částka:</span>
              <span class="font-medium text-blue-900">{{ formatCurrency(goal.current_amount) }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-blue-700">Cílová částka:</span>
              <span class="font-medium text-blue-900">{{ formatCurrency(goal.target_amount) }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-blue-700">Zbývá:</span>
              <span class="font-medium text-blue-900">{{ formatCurrency(remaining) }}</span>
            </div>
          </div>
          
          <!-- Pokrok -->
          <div class="mt-3">
            <div class="w-full bg-blue-200 rounded-full h-2">
              <div
                class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${Math.min((goal.current_amount / goal.target_amount) * 100, 100)}%` }"
              ></div>
            </div>
          </div>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Částka k přidání -->
          <div>
            <label for="amount" class="block text-sm font-medium text-gray-700 mb-2">Částka k přidání (Kč)</label>
            <input
              id="amount"
              v-model.number="form.amount"
              type="number"
              step="0.01"
              min="0.01"
              :max="remaining > 0 ? remaining : undefined"
              required
              class="form-input"
              placeholder="0.00"
              @input="updatePreview"
            />
            <p v-if="remaining > 0" class="text-sm text-gray-500 mt-1">
              Maximálně {{ formatCurrency(remaining) }} do dosažení cíle
            </p>
          </div>

          <!-- Náhled nové částky -->
          <div v-if="form.amount > 0" class="bg-green-50 border border-green-200 rounded-lg p-3">
            <div class="flex items-center justify-between text-sm">
              <span class="text-green-700">Nová částka:</span>
              <span class="font-medium text-green-900">{{ formatCurrency(newAmount) }}</span>
            </div>
            <div class="flex items-center justify-between text-sm mt-1">
              <span class="text-green-700">Nový pokrok:</span>
              <span class="font-medium text-green-900">{{ newProgress }}%</span>
            </div>
            <div v-if="newAmount >= goal.target_amount" class="flex items-center justify-center mt-2">
              <div class="flex items-center space-x-2 text-green-700">
                <CheckCircle class="w-4 h-4" />
                <span class="text-sm font-medium">Cíl bude dokončen! 🎉</span>
              </div>
            </div>
          </div>

          <!-- Chybová zpráva -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
            <div class="flex items-center">
              <AlertCircle class="w-5 h-5 text-red-500 mr-2" />
              <span class="text-sm text-red-700">{{ error }}</span>
            </div>
          </div>

          <!-- Tlačítka -->
          <div class="flex space-x-3 pt-4">
            <button
              type="button"
              @click="$emit('close')"
              class="btn-secondary flex-1"
            >
              Zrušit
            </button>
            <button
              type="submit"
              :disabled="isLoading || !form.amount || form.amount <= 0"
              class="btn-primary flex-1 flex items-center justify-center"
            >
              <div v-if="isLoading" class="loading-spinner mr-2"></div>
              Přidat částku
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import { X, AlertCircle, CheckCircle } from 'lucide-vue-next'

const props = defineProps({
  goal: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'amount-added'])

const financeStore = useFinanceStore()

const isLoading = ref(false)
const error = ref('')

const form = reactive({
  amount: ''
})

const remaining = computed(() => {
  return Math.max(0, props.goal.target_amount - props.goal.current_amount)
})

const newAmount = computed(() => {
  return props.goal.current_amount + (parseFloat(form.amount) || 0)
})

const newProgress = computed(() => {
  if (!form.amount) return Math.round((props.goal.current_amount / props.goal.target_amount) * 100)
  return Math.round((newAmount.value / props.goal.target_amount) * 100)
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('cs-CZ', {
    style: 'currency',
    currency: 'CZK'
  }).format(amount || 0)
}

const updatePreview = () => {
  // Trigger reactivity for computed values
}

const handleSubmit = async () => {
  error.value = ''

  if (!form.amount || form.amount <= 0) {
    error.value = 'Částka musí být větší než 0'
    return
  }

  isLoading.value = true

  try {
    const newCurrentAmount = props.goal.current_amount + parseFloat(form.amount)
    const isCompleted = newCurrentAmount >= props.goal.target_amount

    const result = await financeStore.updateGoal(props.goal.id, {
      ...props.goal,
      current_amount: newCurrentAmount,
      is_completed: isCompleted
    })

    if (result.success) {
      emit('amount-added')
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = 'Došlo k neočekávané chybě'
    console.error('Chyba při přidávání částky k cíli:', err)
  } finally {
    isLoading.value = false
  }
}
</script>