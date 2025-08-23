<template>
  <div class="min-h-mobile safe-top safe-bottom bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <!-- Bottom Navigation pro mobily -->
    <nav class="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 safe-bottom z-50">
      <div class="grid grid-cols-4 gap-1 px-2 py-1">
        <router-link
          v-for="item in navigation"
          :key="item.name"
          :to="item.to"
          class="flex flex-col items-center justify-center py-2 px-1 rounded-lg transition-colors"
          :class="$route.name === item.name ? 'text-blue-600' : 'text-gray-500'"
        >
          <component 
            :is="item.icon" 
            class="w-5 h-5 mb-1"
          />
          <span class="text-xs font-medium">{{ item.label }}</span>
        </router-link>
      </div>
    </nav>

    <!-- Desktop layout -->
    <div class="flex">
      <!-- Sidebar -->
      <div class="hidden lg:flex lg:flex-col lg:w-64 lg:fixed lg:inset-y-0">
        <div class="flex flex-col flex-grow bg-white shadow-sm border-r border-gray-200">
          <!-- Logo -->
          <div class="flex items-center px-6 py-4 border-b border-gray-200">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <TrendingUp class="w-5 h-5 text-white" />
              </div>
              <h1 class="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Yolo Finance
              </h1>
            </div>
          </div>

          <!-- Navigace -->
          <nav class="flex-1 px-4 py-6">
            <div class="space-y-2">
              <router-link
                v-for="item in navigation"
                :key="item.name"
                :to="item.to"
                class="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors group"
                :class="{ 'bg-blue-50 text-blue-700': $route.name === item.name }"
              >
                <component 
                  :is="item.icon" 
                  class="w-5 h-5 transition-colors"
                  :class="$route.name === item.name ? 'text-blue-600' : 'text-gray-500 group-hover:text-gray-700'"
                />
                <span class="font-medium">{{ item.label }}</span>
              </router-link>
            </div>
          </nav>

          <!-- Uživatelské menu -->
          <div class="px-4 py-4 border-t border-gray-200">
            <div class="flex items-center space-x-3 mb-3">
              <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full flex items-center justify-center">
                <span class="text-sm font-medium text-white">
                  {{ userInitials }}
                </span>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 truncate">
                  {{ authStore.userName }}
                </p>
                <p class="text-sm text-gray-500 truncate">
                  {{ authStore.userEmail }}
                </p>
              </div>
            </div>
            <button
              @click="logout"
              class="flex items-center space-x-3 w-full px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
            >
              <LogOut class="w-5 h-5" />
              <span>Odhlásit se</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Hlavní obsah -->
      <div class="lg:pl-64 flex-1">
        <!-- Mobilní header -->
        <div class="lg:hidden bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
          <div class="px-3 sm:px-4 py-2 flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <TrendingUp class="w-5 h-5 text-white" />
              </div>
              <h1 class="text-base sm:text-lg font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Yolo Finance
              </h1>
            </div>
            <button @click="logout" class="p-2 -mr-2 rounded-lg hover:bg-gray-100 active:bg-gray-200">
              <LogOut class="w-5 h-5 text-gray-600" />
            </button>
          </div>
        </div>

        <!-- Obsah stránky -->
        <main class="flex-1">
          <div class="p-3 sm:p-4 lg:p-6 pb-20 lg:pb-6">
            <router-view />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useFinanceStore } from '@/stores/finance'
import {
  Home,
  ArrowUpDown,
  Target,
  PiggyBank,
  TrendingUp,
  LogOut
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const financeStore = useFinanceStore()

// Odstranění nepotřebné reference pro mobilní menu
// const isMobileMenuOpen = ref(false)

const navigation = [
  {
    name: 'Dashboard',
    label: 'Přehled',
    to: '/',
    icon: Home
  },
  {
    name: 'Transactions',
    label: 'Transakce',
    to: '/transakce',
    icon: ArrowUpDown
  },
  {
    name: 'Budgets',
    label: 'Rozpočty',
    to: '/rozpocty',
    icon: PiggyBank
  },
  {
    name: 'Goals',
    label: 'Cíle',
    to: '/cile',
    icon: Target
  }
]

const userInitials = computed(() => {
  const name = authStore.userName
  return name ? name.charAt(0).toUpperCase() : 'U'
})

// Funkce pro mobilní menu už nejsou potřeba
// const openMobileMenu = () => {
//   isMobileMenuOpen.value = true
// }

// const closeMobileMenu = () => {
//   isMobileMenuOpen.value = false
// }

const logout = async () => {
  authStore.logout()
  await router.push('/login')
}

onMounted(() => {
  // Inicializace finančních dat při načtení layout
  financeStore.initializeData()
})
</script>