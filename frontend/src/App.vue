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
  <div id="app" class="min-h-mobile safe-top safe-bottom bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-black transition-colors duration-300">
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
  @apply w-full px-3 py-2.5 sm:px-4 sm:py-3 text-sm sm:text-base text-gray-900 dark:text-white bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:focus:ring-indigo-500 focus:border-transparent transition-all duration-200;
}

.btn-primary {
  @apply bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-500 dark:to-indigo-500 text-white px-4 py-2.5 sm:px-6 sm:py-3 rounded-lg text-sm sm:text-base font-medium hover:from-blue-700 hover:to-indigo-700 dark:hover:from-blue-600 dark:hover:to-indigo-600 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-indigo-400 focus:ring-offset-2 dark:focus:ring-offset-gray-900 transition-all duration-200 active:scale-95;
}

.btn-secondary {
  @apply bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 px-4 py-2.5 sm:px-6 sm:py-3 rounded-lg text-sm sm:text-base font-medium border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 dark:focus:ring-gray-400 focus:ring-offset-2 dark:focus:ring-offset-gray-900 transition-all duration-200 active:scale-95;
}

.card {
  @apply bg-white dark:bg-gray-800 rounded-lg sm:rounded-xl shadow-sm dark:shadow-xl border border-gray-100 dark:border-gray-700 p-4 sm:p-6 transition-all duration-300;
}

.loading-spinner {
  @apply animate-spin rounded-full h-6 w-6 sm:h-8 sm:w-8 border-b-2 border-blue-600 dark:border-indigo-400;
}

/* Mobilní optimalizace */
@media (max-width: 640px) {
  .form-input {
    font-size: 16px; /* Zabránění zoomu na iOS */
  }
}

/* Force layout recalculation on resize */
html, body {
  width: 100%;
  overflow-x: hidden;
}

/* Viewport meta fix for better responsive behavior */
@supports (-webkit-touch-callout: none) {
  /* iOS specific fixes */
  .min-h-mobile {
    min-height: -webkit-fill-available;
  }
}

/* Zajistí správné přepočítání při změně rozlišení */
* {
  transition: none !important;
}

@media screen and (prefers-reduced-motion: no-preference) {
  * {
    transition: all 0.2s ease-in-out !important;
  }
}
</style>
