<template>
  <svg :width="size" :height="size" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="vGradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#c8703f;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#874726;stop-opacity:1" />
      </linearGradient>
    </defs>

    <!-- Background -->
    <rect width="100" height="100" rx="20" fill="url(#vGradient)"/>

    <!-- Letter V, stylized serif -->
    <text
      x="50"
      y="52"
      text-anchor="middle"
      dominant-baseline="central"
      font-family="Georgia, 'Times New Roman', serif"
      font-style="italic"
      font-weight="700"
      font-size="58"
      fill="white"
    >V</text>
  </svg>
</template>

<script setup>
defineProps({
  size: {
    type: [Number, String],
    default: 32
  }
})
</script>
