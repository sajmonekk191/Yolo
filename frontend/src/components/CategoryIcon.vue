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
    required: false
  },
  category: {
    type: String,
    required: false
  },
  color: {
    type: String,
    default: 'gray'
  }
})

const categoryIcons = {
  'Plat': 'Wallet',
  'Mzda': 'Wallet',
  'Freelance': 'Briefcase',
  'Investice': 'TrendingUp',
  'Dary': 'Gift',
  'Ostatní příjem': 'Banknote',
  'Jídlo': 'Utensils',
  'Nakupování': 'ShoppingCart',
  'Bydlení': 'Home',
  'Doprava': 'Car',
  'Zdraví': 'Heart',
  'Oblečení': 'Shirt',
  'Zábava': 'Music',
  'Sport': 'Dumbbell',
  'Cestování': 'Plane',
  'Vzdělání': 'GraduationCap',
  'Elektronika': 'Smartphone',
  'Pojištění': 'Shield',
  'Energie': 'Zap',
  'Splátky': 'CreditCard',
  'Ostatní': 'MoreHorizontal'
}

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

const iconName = computed(() => {
  if (props.icon) return props.icon
  if (props.category) return categoryIcons[props.category] || 'MoreHorizontal'
  return 'MoreHorizontal'
})

const iconComponent = computed(() => iconMap[iconName.value] || MoreHorizontal)

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