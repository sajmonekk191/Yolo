<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Pozadí overlay -->
      <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" @click="$emit('close')"></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-md p-6 my-8 text-left align-middle transition-all transform bg-white shadow-xl rounded-xl">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
              <AlertTriangle class="w-5 h-5 text-red-600" />
            </div>
            <h3 class="text-lg font-semibold text-gray-900">Potvrzení smazání</h3>
          </div>
          <button @click="$emit('close')" class="p-2 text-gray-400 hover:text-gray-600 rounded-lg">
            <X class="w-5 h-5" />
          </button>
        </div>

        <div class="mb-6">
          <h4 v-if="title" class="text-base font-medium text-gray-900 mb-2" v-html="title"></h4>
          <p class="text-gray-600">{{ message }}</p>
        </div>

        <div class="flex space-x-3">
          <button
            @click="$emit('close')"
            class="btn-secondary flex-1"
          >
            Zrušit
          </button>
          <button
            @click="$emit('confirm')"
            class="flex-1 bg-red-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all duration-200"
          >
            Smazat
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { X, AlertTriangle } from 'lucide-vue-next'

defineProps({
  title: {
    type: String,
    default: 'Opravdu chcete pokračovat?'
  },
  message: {
    type: String,
    default: 'Tato akce je nevratná.'
  }
})

defineEmits(['close', 'confirm'])
</script>