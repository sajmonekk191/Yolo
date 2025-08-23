<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(() => {
  authStore.initializeAuth()
})
</script>

<template>
  <div id="app" class="min-h-mobile safe-top safe-bottom bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <RouterView />
  </div>
</template>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Responzivní styly pro formuláře a komponenty */
.form-input {
  @apply w-full px-3 py-2.5 sm:px-4 sm:py-3 text-sm sm:text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200;
}

.btn-primary {
  @apply bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-4 py-2.5 sm:px-6 sm:py-3 rounded-lg text-sm sm:text-base font-medium hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 active:scale-95;
}

.btn-secondary {
  @apply bg-white text-gray-700 px-4 py-2.5 sm:px-6 sm:py-3 rounded-lg text-sm sm:text-base font-medium border border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all duration-200 active:scale-95;
}

.card {
  @apply bg-white rounded-lg sm:rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6;
}

.loading-spinner {
  @apply animate-spin rounded-full h-6 w-6 sm:h-8 sm:w-8 border-b-2 border-blue-600;
}

/* Mobilní optimalizace */
@media (max-width: 640px) {
  .form-input {
    font-size: 16px; /* Zabránění zoomu na iOS */
  }
}
</style>
