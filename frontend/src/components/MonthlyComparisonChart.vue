<template>
  <div class="card">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900">Měsíční srovnání</h3>
      <div class="flex items-center space-x-2">
        <button
          @click="chartType = 'bar'"
          class="p-1.5 rounded-lg transition-colors"
          :class="chartType === 'bar' ? 'bg-indigo-100 text-indigo-600' : 'text-gray-400 hover:text-gray-600'"
        >
          <BarChart3 class="w-4 h-4" />
        </button>
        <button
          @click="chartType = 'line'"
          class="p-1.5 rounded-lg transition-colors"
          :class="chartType === 'line' ? 'bg-indigo-100 text-indigo-600' : 'text-gray-400 hover:text-gray-600'"
        >
          <LineChartIcon class="w-4 h-4" />
        </button>
      </div>
    </div>
    <div class="h-64">
      <component :is="chartComponent" :data="chartData" />
    </div>
    <div class="mt-4 grid grid-cols-3 gap-4 pt-4 border-t border-gray-100">
      <div class="text-center">
        <p class="text-xs text-gray-500">Průměrný příjem</p>
        <p class="text-sm font-semibold text-emerald-600">{{ formatCurrency(averageIncome) }}</p>
      </div>
      <div class="text-center">
        <p class="text-xs text-gray-500">Průměrné výdaje</p>
        <p class="text-sm font-semibold text-rose-600">{{ formatCurrency(averageExpenses) }}</p>
      </div>
      <div class="text-center">
        <p class="text-xs text-gray-500">Průměrné úspory</p>
        <p class="text-sm font-semibold text-indigo-600">{{ formatCurrency(averageSavings) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { BarChart3, LineChart as LineChartIcon } from 'lucide-vue-next'
import BarChart from './BarChart.vue'
import LineChart from './LineChart.vue'

const props = defineProps({
  transactions: {
    type: Array,
    default: () => []
  },
  months: {
    type: Number,
    default: 6
  }
})

const chartType = ref('bar')

const chartComponent = computed(() => {
  return chartType.value === 'bar' ? BarChart : LineChart
})

const monthlyData = computed(() => {
  const data = {}
  const now = new Date()
  
  // Initialize months
  for (let i = props.months - 1; i >= 0; i--) {
    const date = new Date(now.getFullYear(), now.getMonth() - i, 1)
    const key = date.toISOString().substring(0, 7)
    data[key] = { income: 0, expenses: 0 }
  }
  
  // Process transactions
  props.transactions.forEach(t => {
    const month = t.date.substring(0, 7)
    if (data[month]) {
      if (t.type === 'income') {
        data[month].income += t.amount
      } else {
        data[month].expenses += t.amount
      }
    }
  })
  
  return data
})

const chartData = computed(() => {
  const labels = []
  const income = []
  const expenses = []
  const savings = []
  
  Object.entries(monthlyData.value).forEach(([month, data]) => {
    const date = new Date(month + '-01')
    labels.push(date.toLocaleDateString('cs-CZ', { month: 'short' }))
    income.push(data.income)
    expenses.push(data.expenses)
    savings.push(data.income - data.expenses)
  })
  
  return {
    labels,
    datasets: [
      {
        label: 'Příjmy',
        data: income,
        backgroundColor: chartType.value === 'bar' ? 'rgba(16, 185, 129, 0.8)' : 'rgba(16, 185, 129, 0.1)',
        borderColor: 'rgb(16, 185, 129)',
        borderWidth: 2,
        tension: 0.4,
        fill: chartType.value === 'line'
      },
      {
        label: 'Výdaje',
        data: expenses,
        backgroundColor: chartType.value === 'bar' ? 'rgba(244, 63, 94, 0.8)' : 'rgba(244, 63, 94, 0.1)',
        borderColor: 'rgb(244, 63, 94)',
        borderWidth: 2,
        tension: 0.4,
        fill: chartType.value === 'line'
      },
      {
        label: 'Úspory',
        data: savings,
        backgroundColor: chartType.value === 'bar' ? 'rgba(99, 102, 241, 0.8)' : 'rgba(99, 102, 241, 0.1)',
        borderColor: 'rgb(99, 102, 241)',
        borderWidth: 2,
        tension: 0.4,
        fill: chartType.value === 'line'
      }
    ]
  }
})

const averageIncome = computed(() => {
  const values = chartData.value.datasets[0].data
  return values.reduce((a, b) => a + b, 0) / values.length
})

const averageExpenses = computed(() => {
  const values = chartData.value.datasets[1].data
  return values.reduce((a, b) => a + b, 0) / values.length
})

const averageSavings = computed(() => {
  return averageIncome.value - averageExpenses.value
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('cs-CZ', {
    style: 'currency',
    currency: 'CZK',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount || 0)
}
</script>