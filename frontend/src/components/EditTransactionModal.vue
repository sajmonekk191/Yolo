<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Pozadí overlay -->
      <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" @click="$emit('close')"></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-md p-6 my-8 text-left align-middle transition-all transform bg-white shadow-xl rounded-xl">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Upravit transakci</h3>
          <button @click="$emit('close')" class="p-2 text-gray-400 hover:text-gray-600 rounded-lg">
            <X class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Typ transakce -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Typ transakce</label>
            <div class="grid grid-cols-2 gap-3">
              <button
                type="button"
                @click="form.type = 'income'"
                class="p-3 rounded-lg border text-center transition-colors"
                :class="form.type === 'income' 
                  ? 'border-green-500 bg-green-50 text-green-700' 
                  : 'border-gray-300 text-gray-700 hover:bg-gray-50'"
              >
                <TrendingUp class="w-5 h-5 mx-auto mb-1" />
                <span class="text-sm font-medium">Příjem</span>
              </button>
              <button
                type="button"
                @click="form.type = 'expense'"
                class="p-3 rounded-lg border text-center transition-colors"
                :class="form.type === 'expense' 
                  ? 'border-red-500 bg-red-50 text-red-700' 
                  : 'border-gray-300 text-gray-700 hover:bg-gray-50'"
              >
                <TrendingDown class="w-5 h-5 mx-auto mb-1" />
                <span class="text-sm font-medium">Výdaj</span>
              </button>
            </div>
          </div>

          <!-- Částka -->
          <div>
            <label for="amount" class="block text-sm font-medium text-gray-700 mb-2">Částka (Kč)</label>
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

          <!-- Popis -->
          <div>
            <label for="description" class="block text-sm font-medium text-gray-700 mb-2">Popis</label>
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
            <label for="category" class="block text-sm font-medium text-gray-700 mb-2">Kategorie</label>
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
            <label for="date" class="block text-sm font-medium text-gray-700 mb-2">Datum</label>
            <input
              id="date"
              v-model="form.date"
              type="date"
              required
              class="form-input"
            />
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
              Uložit
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import { X, TrendingUp, TrendingDown, AlertCircle } from 'lucide-vue-next'

const props = defineProps({
  transaction: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'transaction-updated'])

const financeStore = useFinanceStore()

const isLoading = ref(false)
const error = ref('')

const form = reactive({
  type: '',
  amount: '',
  description: '',
  category_id: '',
  date: ''
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
    const result = await financeStore.updateTransaction(props.transaction.id, {
      type: form.type,
      amount: parseFloat(form.amount),
      description: form.description,
      category_id: parseInt(form.category_id),
      date: form.date
    })

    if (result.success) {
      emit('transaction-updated')
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = 'Došlo k neočekávané chybě'
    console.error('Chyba při aktualizaci transakce:', err)
  } finally {
    isLoading.value = false
  }
}

// Reset kategorie při změně typu
watch(() => form.type, () => {
  // Pokud aktuální kategorie nepatří do nového typu, vymaž ji
  const currentCategory = financeStore.categories.find(c => c.id === parseInt(form.category_id))
  if (currentCategory && currentCategory.type !== form.type) {
    form.category_id = ''
  }
})

onMounted(() => {
  // Naplň formulář daty z transakce
  form.type = props.transaction.type
  form.amount = props.transaction.amount
  form.description = props.transaction.description
  form.category_id = props.transaction.category_id
  form.date = props.transaction.date
})
</script>