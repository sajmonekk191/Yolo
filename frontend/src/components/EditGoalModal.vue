<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Pozadí overlay -->
      <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" @click="$emit('close')"></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-md p-6 my-8 text-left align-middle transition-all transform bg-white shadow-xl rounded-xl">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Upravit cíl</h3>
          <button @click="$emit('close')" class="p-2 text-gray-400 hover:text-gray-600 rounded-lg">
            <X class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Název cíle -->
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">Název cíle</label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="form-input"
              placeholder="Např. Dovolená, Nové auto..."
            />
          </div>

          <!-- Popis -->
          <div>
            <label for="description" class="block text-sm font-medium text-gray-700 mb-2">Popis (nepovinný)</label>
            <textarea
              id="description"
              v-model="form.description"
              rows="3"
              class="form-input"
              placeholder="Detailní popis vašeho cíle..."
            ></textarea>
          </div>

          <!-- Cílová částka -->
          <div>
            <label for="target_amount" class="block text-sm font-medium text-gray-700 mb-2">Cílová částka (Kč)</label>
            <input
              id="target_amount"
              v-model.number="form.target_amount"
              type="number"
              step="0.01"
              min="0"
              required
              class="form-input"
              placeholder="0.00"
            />
          </div>

          <!-- Aktuální částka -->
          <div>
            <label for="current_amount" class="block text-sm font-medium text-gray-700 mb-2">Aktuální částka (Kč)</label>
            <input
              id="current_amount"
              v-model.number="form.current_amount"
              type="number"
              step="0.01"
              min="0"
              class="form-input"
              placeholder="0.00"
            />
          </div>

          <!-- Cílové datum -->
          <div>
            <label for="target_date" class="block text-sm font-medium text-gray-700 mb-2">Cílové datum</label>
            <input
              id="target_date"
              v-model="form.target_date"
              type="date"
              required
              class="form-input"
            />
          </div>

          <!-- Stav dokončení -->
          <div class="flex items-center space-x-3">
            <input
              id="is_completed"
              v-model="form.is_completed"
              type="checkbox"
              class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label for="is_completed" class="text-sm font-medium text-gray-700">
              Označit jako dokončený
            </label>
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
              :disabled="isLoading"
              class="btn-primary flex-1 flex items-center justify-center"
            >
              <div v-if="isLoading" class="loading-spinner mr-2"></div>
              Uložit změny
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import { X, AlertCircle } from 'lucide-vue-next'

const props = defineProps({
  goal: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'goal-updated'])

const financeStore = useFinanceStore()

const isLoading = ref(false)
const error = ref('')

const form = reactive({
  name: '',
  description: '',
  target_amount: '',
  current_amount: '',
  target_date: '',
  is_completed: false
})

const handleSubmit = async () => {
  error.value = ''

  // Validace
  if (parseFloat(form.current_amount) > parseFloat(form.target_amount)) {
    error.value = 'Aktuální částka nemůže být vyšší než cílová částka'
    return
  }

  isLoading.value = true

  try {
    const result = await financeStore.updateGoal(props.goal.id, {
      name: form.name,
      description: form.description,
      target_amount: parseFloat(form.target_amount),
      current_amount: parseFloat(form.current_amount),
      target_date: form.target_date,
      is_completed: form.is_completed
    })

    if (result.success) {
      emit('goal-updated')
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = 'Došlo k neočekávané chybě'
    console.error('Chyba při aktualizaci cíle:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  // Naplň formulář daty z cíle
  form.name = props.goal.name
  form.description = props.goal.description || ''
  form.target_amount = props.goal.target_amount
  form.current_amount = props.goal.current_amount
  form.target_date = props.goal.target_date
  form.is_completed = props.goal.is_completed
})
</script>