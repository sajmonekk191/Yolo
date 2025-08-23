<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 100 100"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    :class="className"
  >
    <!-- Gradient definitions -->
    <defs>
      <linearGradient id="iconGradient1" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#6366F1;stop-opacity:1" />
      </linearGradient>
      <linearGradient id="iconGradient2" x1="0%" y1="100%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#8B5CF6;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#3B82F6;stop-opacity:1" />
      </linearGradient>
      <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
        <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.1"/>
      </filter>
    </defs>

    <!-- Background circle or rounded square -->
    <rect
      v-if="showBackground && variant !== 'minimal'"
      x="5"
      y="5"
      width="90"
      height="90"
      rx="22"
      fill="url(#iconGradient1)"
      filter="url(#shadow)"
    />
    <circle
      v-else-if="showBackground && variant === 'minimal'"
      cx="50"
      cy="50"
      r="45"
      fill="url(#iconGradient1)"
      filter="url(#shadow)"
    />

    <!-- Y letter stylized as chart -->
    <g v-if="variant === 'default'">
      <!-- Stylized Y with thicker strokes -->
      <path
        d="M25 20 L50 50 L50 75 M75 20 L50 50"
        stroke="white"
        stroke-width="5"
        stroke-linecap="round"
        stroke-linejoin="round"
        fill="none"
      />
      <!-- Rising chart overlay -->
      <rect x="30" y="55" width="5" height="12" fill="white" opacity="0.6" rx="2" />
      <rect x="38" y="48" width="5" height="19" fill="white" opacity="0.7" rx="2" />
      <rect x="46" y="42" width="5" height="25" fill="white" opacity="0.8" rx="2" />
      <rect x="54" y="35" width="5" height="32" fill="white" opacity="0.6" rx="2" />
      <rect x="62" y="30" width="5" height="37" fill="white" opacity="0.5" rx="2" />
      <!-- Central dot accent -->
      <circle cx="50" cy="50" r="3" fill="white" />
    </g>

    <!-- Minimalist variant -->
    <g v-else-if="variant === 'minimal'">
      <path
        d="M30 20 L50 50 L50 80 M70 20 L50 50"
        stroke="url(#iconGradient2)"
        stroke-width="4"
        stroke-linecap="round"
        stroke-linejoin="round"
        fill="none"
      />
      <circle cx="50" cy="50" r="4" fill="url(#iconGradient2)" />
    </g>

    <!-- Currency variant -->
    <g v-else-if="variant === 'currency'">
      <!-- Y shape -->
      <path
        d="M25 20 L50 50 L50 75 M75 20 L50 50"
        stroke="white"
        stroke-width="4"
        stroke-linecap="round"
        stroke-linejoin="round"
        fill="none"
      />
      <!-- Currency symbols -->
      <text x="30" y="30" fill="white" font-size="12" font-weight="bold" opacity="0.8">$</text>
      <text x="65" y="30" fill="white" font-size="12" font-weight="bold" opacity="0.8">€</text>
      <text x="47" y="85" fill="white" font-size="12" font-weight="bold" opacity="0.8">¥</text>
    </g>
  </svg>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  size: {
    type: [Number, String],
    default: 40
  },
  variant: {
    type: String,
    default: 'default', // 'default', 'minimal', 'currency'
    validator: (value) => ['default', 'minimal', 'currency'].includes(value)
  },
  showBackground: {
    type: Boolean,
    default: true
  },
  className: {
    type: String,
    default: ''
  }
})
</script>