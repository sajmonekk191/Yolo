<template>
  <component
    :is="iconComponent"
    :class="[
      'w-5 h-5',
      colorClass
    ]"
  />
</template>

<script setup>
import { computed } from 'vue'
import {
  Banknote,
  Briefcase,
  TrendingUp,
  Gift,
  Wallet,
  ShoppingCart,
  Home,
  Car,
  Heart,
  Shirt,
  Music,
  Utensils,
  Dumbbell,
  Plane,
  GraduationCap,
  Smartphone,
  Shield,
  Zap,
  CreditCard,
  MoreHorizontal
} from 'lucide-vue-next'

const props = defineProps({
  icon: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: 'gray'
  }
})

const iconMap = {
  Banknote,
  Briefcase,
  TrendingUp,
  Gift,
  Wallet,
  ShoppingCart,
  Home,
  Car,
  Heart,
  Shirt,
  Music,
  Utensils,
  Dumbbell,
  Plane,
  GraduationCap,
  Smartphone,
  Shield,
  Zap,
  CreditCard,
  MoreHorizontal
}

const iconComponent = computed(() => iconMap[props.icon] || MoreHorizontal)

const colorClass = computed(() => {
  const colors = {
    green: 'text-green-600',
    blue: 'text-blue-600',
    purple: 'text-purple-600',
    pink: 'text-pink-600',
    orange: 'text-orange-600',
    indigo: 'text-indigo-600',
    red: 'text-red-600',
    yellow: 'text-yellow-600',
    cyan: 'text-cyan-600',
    gray: 'text-gray-600'
  }
  return colors[props.color] || 'text-gray-600'
})
</script>