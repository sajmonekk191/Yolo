<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  stacked: {
    type: Boolean,
    default: false
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
      position: 'top',
      labels: {
        color: '#6b7280',
        font: {
          size: 12
        }
      }
    },
    title: {
      display: !!props.title,
      text: props.title,
      color: '#111827',
      font: {
        size: 16,
        weight: 'bold'
      }
    },
    tooltip: {
      mode: 'index',
      intersect: false,
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
          let label = context.dataset.label || ''
          if (label) {
            label += ': '
          }
          label += context.parsed.y.toLocaleString('cs-CZ') + ' Kč'
          return label
        }
      }
    }
  },
  scales: {
    x: {
      stacked: props.stacked,
      grid: {
        display: false
      },
      ticks: {
        color: '#6b7280',
        font: {
          size: 11
        }
      }
    },
    y: {
      stacked: props.stacked,
      grid: {
        color: 'rgba(229, 231, 235, 0.5)'
      },
      ticks: {
        color: '#6b7280',
        font: {
          size: 11
        },
        callback: function(value) {
          return value.toLocaleString('cs-CZ') + ' Kč'
        }
      }
    }
  }
}
</script>