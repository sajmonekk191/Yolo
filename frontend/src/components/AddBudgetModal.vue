<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Pozadí overlay -->
      <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" @click="$emit('close')"></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-md p-6 my-8 text-left align-middle transition-all transform bg-white shadow-xl rounded-xl">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Přidat nový rozpočet</h3>
          <button @click="$emit('close')" class="p-2 text-gray-400 hover:text-gray-600 rounded-lg">
            <X class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Kategorie -->
          <div>
            <label for="category" class="block text-sm font-medium text-gray-700 mb-2">Kategorie</label>
            <select
              id="category"
              v-model="form.category_id"
              required
              class="form-input"
            >
              <option value="">Vyberte kategorii</option>
              <option
                v-for="category in financeStore.expenseCategories"
                :key="category.id"
                :value="category.id"
              >
                {{ category.name }}
              </option>
            </select>
          </div>

          <!-- Částka rozpočtu -->
          <div>
            <label for="amount" class="block text-sm font-medium text-gray-700 mb-2">Částka rozpočtu (Kč)</label>
            <input
              id="amount"
              v-model.number="form.amount"
              type="number"
              step="0.01"
              min="0"
              required
              class="form-input"
              placeholder="0.00"
            />
          </div>

          <!-- Měsíc -->
          <div>
            <label for="month" class="block text-sm font-medium text-gray-700 mb-2">Měsíc</label>
            <select
              id="month"
              v-model="form.month"
              required
              class="form-input"
            >
              <option
                v-for="(monthName, index) in months"
                :key="index"
                :value="index + 1"
              >
                {{ monthName }}
              </option>
            </select>
          </div>

          <!-- Rok -->
          <div>
            <label for="year" class="block text-sm font-medium text-gray-700 mb-2">Rok</label>
            <select
              id="year"
              v-model="form.year"
              required
              class="form-input"
            >
              <option
                v-for="year in availableYears"
                :key="year"
                :value="year"
              >
                {{ year }}
              </option>
            </select>
          </div>

          <!-- Aktivní -->
          <div class="flex items-center space-x-3">
            <input
              id="is_active"
              v-model="form.is_active"
              type="checkbox"
              class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label for="is_active" class="text-sm font-medium text-gray-700">
              Aktivní rozpočet
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
              Vytvořit rozpočet
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import { X, AlertCircle } from 'lucide-vue-next'

const emit = defineEmits(['close', 'budget-added'])

const financeStore = useFinanceStore()

const isLoading = ref(false)
const error = ref('')

const form = reactive({
  category_id: '',
  amount: '',
  month: new Date().getMonth() + 1, // Aktuální měsíc
  year: new Date().getFullYear(), // Aktuální rok
  is_active: true
})

const months = [
  'Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen',
  'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec'
]

const availableYears = computed(() => {
  const currentYear = new Date().getFullYear()
  const years = []
  for (let i = currentYear - 1; i <= currentYear + 2; i++) {
    years.push(i)
  }
  return years
})

const handleSubmit = async () => {
  error.value = ''

  // Kontrola duplicity
  const existingBudget = financeStore.budgets.find(b => 
    b.category_id === parseInt(form.category_id) && 
    b.month === form.month && 
    b.year === form.year
  )

  if (existingBudget) {
    error.value = 'Rozpočet pro tuto kategorii a období již existuje'
    return
  }

  isLoading.value = true

  try {
    const result = await financeStore.createBudget({
      category_id: parseInt(form.category_id),
      amount: parseFloat(form.amount),
      month: form.month,
      year: form.year,
      is_active: form.is_active
    })

    if (result.success) {
      emit('budget-added')
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = 'Došlo k neočekávané chybě'
    console.error('Chyba při vytváření rozpočtu:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  // Načti kategorie pokud nejsou načtené
  if (financeStore.categories.length === 0) {
    financeStore.fetchCategories()
  }
})
</script>