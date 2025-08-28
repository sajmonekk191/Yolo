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
  // České názvy
  'Plat': 'Wallet',
  'Mzda': 'Wallet',
  'Freelance': 'Briefcase',
  'Investice': 'TrendingUp',
  'Dary': 'Gift',
  'Ostatní příjem': 'Banknote',
  'Ostatní příjmy': 'Banknote',
  'Jídlo': 'Utensils',
  'Jídlo a potraviny': 'ShoppingCart',
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
  'Telefon a internet': 'Smartphone',
  'Pojištění': 'Shield',
  'Energie': 'Zap',
  'Splátky': 'CreditCard',
  'Předplatné': 'CreditCard',
  'Restaurace': 'Utensils',
  'Ostatní': 'MoreHorizontal',
  'Ostatní výdaje': 'MoreHorizontal'
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

const categoryColors = {
  'Jídlo a potraviny': 'orange',
  'Doprava': 'indigo',
  'Zábava': 'pink',
  'Energie': 'yellow',
  'Bydlení': 'blue',
  'Zdraví': 'red',
  'Oblečení': 'purple',
  'Sport': 'green',
  'Cestování': 'cyan',
  'Vzdělání': 'blue',
  'Telefon a internet': 'gray',
  'Pojištění': 'green',
  'Předplatné': 'purple',
  'Restaurace': 'yellow'
}

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
  
  // Pokud není specifikována barva, zkusíme ji určit podle kategorie
  let colorToUse = props.color
  if (!colorToUse && props.category) {
    colorToUse = categoryColors[props.category] || 'gray'
  }
  
  return colors[colorToUse] || 'text-gray-600'
})
</script>