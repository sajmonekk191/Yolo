<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo a nadpis -->
      <div class="text-center">
        <div class="flex justify-center mb-6">
          <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg">
            <TrendingUp class="w-8 h-8 text-white" />
          </div>
        </div>
        <h2 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
          Yolo Finance
        </h2>
        <p class="mt-2 text-gray-600">
          {{ isLogin ? 'Přihlaste se do svého účtu' : 'Vytvořte si nový účet' }}
        </p>
      </div>

      <!-- Formulář -->
      <div class="card">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Jméno (pouze při registraci) -->
          <div v-if="!isLogin">
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
              Celé jméno
            </label>
            <div class="relative">
              <User class="absolute left-3 top-3 w-5 h-5 text-gray-400" />
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                class="form-input pl-10"
                placeholder="Jan Novák"
              />
            </div>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <div class="relative">
              <Mail class="absolute left-3 top-3 w-5 h-5 text-gray-400" />
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="form-input pl-10"
                placeholder="jan@example.com"
              />
            </div>
          </div>

          <!-- Heslo -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Heslo
            </label>
            <div class="relative">
              <Lock class="absolute left-3 top-3 w-5 h-5 text-gray-400" />
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="form-input pl-10 pr-10"
                placeholder="••••••••"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
              >
                <Eye v-if="!showPassword" class="w-5 h-5" />
                <EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>

          <!-- Potvrzení hesla (pouze při registraci) -->
          <div v-if="!isLogin">
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Potvrzení hesla
            </label>
            <div class="relative">
              <Lock class="absolute left-3 top-3 w-5 h-5 text-gray-400" />
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                type="password"
                required
                class="form-input pl-10"
                placeholder="••••••••"
              />
            </div>
          </div>

          <!-- Chybová zpráva -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
            <div class="flex items-center">
              <AlertCircle class="w-5 h-5 text-red-500 mr-2" />
              <span class="text-sm text-red-700">{{ error }}</span>
            </div>
          </div>

          <!-- Úspěšná zpráva -->
          <div v-if="success" class="bg-green-50 border border-green-200 rounded-lg p-3">
            <div class="flex items-center">
              <CheckCircle class="w-5 h-5 text-green-500 mr-2" />
              <span class="text-sm text-green-700">{{ success }}</span>
            </div>
          </div>

          <!-- Tlačítko odeslání -->
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="btn-primary w-full flex items-center justify-center"
          >
            <div v-if="authStore.isLoading" class="loading-spinner mr-2"></div>
            {{ isLogin ? 'Přihlásit se' : 'Registrovat se' }}
          </button>
        </form>

        <!-- Přepínání mezi přihlášením a registrací -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            {{ isLogin ? 'Nemáte účet?' : 'Už máte účet?' }}
            <button
              @click="toggleMode"
              class="text-blue-600 hover:text-blue-500 font-medium ml-1"
            >
              {{ isLogin ? 'Registrujte se' : 'Přihlaste se' }}
            </button>
          </p>
        </div>
      </div>

      <!-- Demo přihlašovací údaje -->
      <div class="card bg-blue-50 border-blue-200">
        <h3 class="text-sm font-medium text-blue-900 mb-2">Demo přihlášení</h3>
        <p class="text-sm text-blue-700 mb-3">Pro testování můžete použít:</p>
        <div class="text-sm text-blue-700 space-y-1">
          <p><span class="font-medium">Email:</span> demo@yolo-finance.cz</p>
          <p><span class="font-medium">Heslo:</span> demo123</p>
        </div>
        <button
          @click="fillDemoData"
          class="mt-3 text-sm text-blue-600 hover:text-blue-500 underline"
        >
          Vyplnit demo údaje
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  TrendingUp,
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
  AlertCircle,
  CheckCircle
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const isLogin = ref(true)
const showPassword = ref(false)
const error = ref('')
const success = ref('')

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
  success.value = ''
  resetForm()
}

const resetForm = () => {
  form.name = ''
  form.email = ''
  form.password = ''
  form.confirmPassword = ''
}

const fillDemoData = () => {
  form.email = 'demo@yolo-finance.cz'
  form.password = 'demo123'
  isLogin.value = true
}

const validateForm = () => {
  if (!isLogin.value) {
    if (!form.name.trim()) {
      error.value = 'Jméno je povinné'
      return false
    }
    if (form.password !== form.confirmPassword) {
      error.value = 'Hesla se neshodují'
      return false
    }
    if (form.password.length < 6) {
      error.value = 'Heslo musí mít alespoň 6 znaků'
      return false
    }
  }
  return true
}

const handleSubmit = async () => {
  error.value = ''
  success.value = ''

  if (!validateForm()) {
    return
  }

  try {
    if (isLogin.value) {
      // Přihlášení
      const result = await authStore.login({
        email: form.email,
        password: form.password
      })

      if (result.success) {
        await router.push('/')
      } else {
        error.value = result.error
      }
    } else {
      // Registrace
      const result = await authStore.register({
        username: form.name,
        email: form.email,
        password: form.password
      })

      if (result.success) {
        success.value = 'Účet byl úspěšně vytvořen! Nyní se můžete přihlásit.'
        isLogin.value = true
        form.name = ''
        form.confirmPassword = ''
      } else {
        error.value = result.error
      }
    }
  } catch (err) {
    error.value = 'Došlo k neočekávané chybě. Zkuste to znovu.'
    console.error('Chyba při autentizaci:', err)
  }
}
</script>