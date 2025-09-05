import { ref, watch, onMounted } from 'vue'

const isDarkMode = ref(false)

export function useDarkMode() {
  // Inicializace dark mode z localStorage nebo system preference
  const initDarkMode = () => {
    // Zkontroluj localStorage
    const stored = localStorage.getItem('darkMode')
    if (stored !== null) {
      isDarkMode.value = stored === 'true'
    } else {
      // Pokud není v localStorage, použij system preference
      isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    
    // Aplikuj dark mode class na HTML element
    updateDarkMode()
  }

  // Toggle dark mode
  const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value
  }

  // Update DOM a localStorage
  const updateDarkMode = () => {
    if (isDarkMode.value) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('darkMode', 'true')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('darkMode', 'false')
    }
  }

  // Watch změny
  watch(isDarkMode, updateDarkMode)

  // Poslouchej system preference změny
  onMounted(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', (e) => {
      // Pouze pokud není nastaveno v localStorage
      if (localStorage.getItem('darkMode') === null) {
        isDarkMode.value = e.matches
      }
    })
  })

  return {
    isDarkMode,
    toggleDarkMode,
    initDarkMode
  }
}