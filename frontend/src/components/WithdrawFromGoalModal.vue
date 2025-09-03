<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-lg max-w-md w-full">
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-xl font-semibold text-gray-900">Vybrat z cíle</h2>
        <p class="text-sm text-gray-500 mt-1">Přesunout peníze zpět na dostupný účet</p>
      </div>

      <div class="p-6 space-y-4">
        <!-- Info o cíli -->
        <div class="bg-gray-50 p-4 rounded-lg">
          <h3 class="font-medium text-gray-900">{{ goal.name }}</h3>
          <p class="text-sm text-gray-600 mt-1">{{ goal.description }}</p>
          <div class="mt-3 space-y-1">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Aktuálně v cíli:</span>
              <span class="font-semibold text-gray-900">{{ formatCurrency(goal.current_amount) }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Cílová částka:</span>
              <span class="text-gray-700">{{ formatCurrency(goal.target_amount) }}</span>
            </div>
          </div>
        </div>

        <!-- Částka k výběru -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Částka k výběru
          </label>
          <div class="relative">
            <input
              v-model.number="amount"
              type="number"
              min="0"
              :max="goal.current_amount"
              placeholder="0"
              class="form-input w-full pr-12"
              @input="validateAmount"
            />
            <span class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-500">
              Kč
            </span>
          </div>
          <p v-if="amountError" class="text-red-500 text-sm mt-1">{{ amountError }}</p>
        </div>

        <!-- Rychlé volby -->
        <div class="flex gap-2">
          <button
            @click="setPercentage(25)"
            class="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
          >
            25%
          </button>
          <button
            @click="setPercentage(50)"
            class="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
          >
            50%
          </button>
          <button
            @click="setPercentage(75)"
            class="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
          >
            75%
          </button>
          <button
            @click="setPercentage(100)"
            class="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Vše
          </button>
        </div>

        <!-- Důvod výběru (volitelné) -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Důvod výběru (volitelné)
          </label>
          <textarea
            v-model="reason"
            rows="2"
            class="form-input w-full"
            placeholder="Např. Nečekaný výdaj, změna priorit..."
          ></textarea>
        </div>
      </div>

      <div class="p-6 border-t border-gray-200 flex justify-end space-x-3">
        <button
          @click="$emit('close')"
          class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
        >
          Zrušit
        </button>
        <button
          @click="handleWithdraw"
          :disabled="!isValid || isLoading"
          class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading">Zpracovávám...</span>
          <span v-else>Vybrat {{ formatCurrency(amount || 0) }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useFinanceStore } from '@/stores/finance'

const props = defineProps({
  goal: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'withdrawn'])

const financeStore = useFinanceStore()

const amount = ref(0)
const reason = ref('')
const amountError = ref('')
const isLoading = ref(false)

const isValid = computed(() => {
  return amount.value > 0 && 
         amount.value <= props.goal.current_amount && 
         !amountError.value
})

const validateAmount = () => {
  if (amount.value < 0) {
    amountError.value = 'Částka musí být kladná'
  } else if (amount.value > props.goal.current_amount) {
    amountError.value = 'Nedostatek peněz v cíli'
  } else {
    amountError.value = ''
  }
}

const setPercentage = (percentage) => {
  amount.value = Math.floor(props.goal.current_amount * percentage / 100)
  validateAmount()
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('cs-CZ', {
    style: 'currency',
    currency: 'CZK',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value || 0)
}

const handleWithdraw = async () => {
  if (!isValid.value) return

  isLoading.value = true
  try {
    const result = await financeStore.withdrawFromGoal(props.goal.id, amount.value)
    
    if (result.success) {
      emit('withdrawn', {
        goalId: props.goal.id,
        amount: amount.value,
        reason: reason.value
      })
      emit('close')
    } else {
      amountError.value = result.error || 'Chyba při výběru'
    }
  } catch (error) {
    console.error('Chyba při výběru z cíle:', error)
    amountError.value = 'Nastala chyba při zpracování'
  } finally {
    isLoading.value = false
  }
}
</script>