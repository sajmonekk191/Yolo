<template>
  <Doughnut :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  title: {
    type: String,
    default: ''
  }
})

const chartData = {
  labels: props.data.labels,
  datasets: props.data.datasets
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#6b7280',
        font: {
          size: 12
        },
        padding: 15
      }
    },
    title: {
      display: !!props.title,
      text: props.title,
      color: '#111827',
      font: {
        size: 16,
        weight: 'bold'
      },
      padding: {
        bottom: 10
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleFont: {
        size: 13
      },
      bodyFont: {
        size: 12
      },
      padding: 10,
      cornerRadius: 8,
      callbacks: {
        label: function(context) {
          const label = context.label || ''
          const value = context.parsed || 0
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const percentage = ((value / total) * 100).toFixed(1)
          return `${label}: ${value.toLocaleString('cs-CZ')} Kč (${percentage}%)`
        }
      }
    }
  }
}
</script>