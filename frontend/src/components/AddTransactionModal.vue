<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end sm:items-center justify-center min-h-screen text-center">
      <!-- Pozadí overlay -->
      <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" @click="$emit('close')"></div>

      <!-- Modal panel -->
      <div class="inline-block w-full sm:max-w-md p-4 sm:p-6 sm:my-8 text-left align-bottom sm:align-middle transition-all transform bg-white shadow-xl rounded-t-2xl sm:rounded-xl safe-bottom">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-base sm:text-lg font-semibold text-gray-900">Přidat transakci</h3>
          <button @click="$emit('close')" class="p-1.5 sm:p-2 text-gray-400 hover:text-gray-600 rounded-lg">
            <X class="w-4 h-4 sm:w-5 sm:h-5" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Typ transakce -->
          <div>
            <label class="block text-xs sm:text-sm font-medium text-gray-700 mb-2">Typ transakce</label>
            <div class="grid grid-cols-2 gap-2 sm:gap-3">
              <button
                type="button"
                @click="form.type = 'income'"
                class="p-2.5 sm:p-3 rounded-lg border text-center transition-colors"
                :class="form.type === 'income' 
                  ? 'border-green-500 bg-green-50 text-green-700' 
                  : 'border-gray-300 text-gray-700 hover:bg-gray-50'"
              >
                <TrendingUp class="w-4 h-4 sm:w-5 sm:h-5 mx-auto mb-1" />
                <span class="text-xs sm:text-sm font-medium">Příjem</span>
              </button>
              <button
                type="button"
                @click="form.type = 'expense'"
                class="p-2.5 sm:p-3 rounded-lg border text-center transition-colors"
                :class="form.type === 'expense' 
                  ? 'border-red-500 bg-red-50 text-red-700' 
                  : 'border-gray-300 text-gray-700 hover:bg-gray-50'"
              >
                <TrendingDown class="w-4 h-4 sm:w-5 sm:h-5 mx-auto mb-1" />
                <span class="text-xs sm:text-sm font-medium">Výdaj</span>
              </button>
            </div>
          </div>

          <!-- Částka -->
          <div>
            <label for="amount" class="block text-xs sm:text-sm font-medium text-gray-700 mb-1.5 sm:mb-2">Částka (Kč)</label>
            <input
              id="amount"
              v-model.number="form.amount"
              type="number"
              step="0.01"
              min="0"
              required
              class="form-input"
              placeholder="0.00"
              inputmode="decimal"
            />
          </div>

          <!-- Popis -->
          <div>
            <label for="description" class="block text-xs sm:text-sm font-medium text-gray-700 mb-1.5 sm:mb-2">Popis</label>
            <input
              id="description"
              v-model="form.description"
              type="text"
              required
              class="form-input"
              placeholder="Popis transakce"
            />
          </div>

          <!-- Kategorie -->
          <div>
            <label for="category" class="block text-xs sm:text-sm font-medium text-gray-700 mb-1.5 sm:mb-2">Kategorie</label>
            <select
              id="category"
              v-model="form.category_id"
              required
              class="form-input"
            >
              <option value="">Vyberte kategorii</option>
              <option
                v-for="category in availableCategories"
                :key="category.id"
                :value="category.id"
              >
                {{ category.name }}
              </option>
            </select>
          </div>

          <!-- Datum -->
          <div>
            <label for="date" class="block text-xs sm:text-sm font-medium text-gray-700 mb-1.5 sm:mb-2">Datum</label>
            <input
              id="date"
              v-model="form.date"
              type="date"
              required
              class="form-input"
            />
          </div>

          <!-- Chybová zpráva -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-2.5 sm:p-3">
            <div class="flex items-center">
              <AlertCircle class="w-4 h-4 sm:w-5 sm:h-5 text-red-500 mr-2 flex-shrink-0" />
              <span class="text-xs sm:text-sm text-red-700">{{ error }}</span>
            </div>
          </div>

          <!-- Tlačítka -->
          <div class="flex space-x-2 sm:space-x-3 pt-3 sm:pt-4">
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
              Přidat
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import { X, TrendingUp, TrendingDown, AlertCircle } from 'lucide-vue-next'

const emit = defineEmits(['close', 'transaction-added'])

const financeStore = useFinanceStore()

const isLoading = ref(false)
const error = ref('')

const form = reactive({
  type: 'expense',
  amount: '',
  description: '',
  category_id: '',
  date: new Date().toISOString().split('T')[0] // Dnešní datum
})

const availableCategories = computed(() => {
  return form.type === 'income' 
    ? financeStore.incomeCategories 
    : financeStore.expenseCategories
})

const handleSubmit = async () => {
  error.value = ''
  isLoading.value = true

  try {
    const result = await financeStore.createTransaction({
      type: form.type,
      amount: parseFloat(form.amount),
      description: form.description,
      category_id: parseInt(form.category_id),
      date: form.date
    })

    if (result.success) {
      emit('transaction-added')
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = 'Došlo k neočekávané chybě'
    console.error('Chyba při vytváření transakce:', err)
  } finally {
    isLoading.value = false
  }
}

// Reset kategorie při změně typu
watch(() => form.type, () => {
  form.category_id = ''
})

onMounted(() => {
  // Načti kategorie pokud nejsou načtené
  if (financeStore.categories.length === 0) {
    financeStore.fetchCategories()
  }
})
</script>