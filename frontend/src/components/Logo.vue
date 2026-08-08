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

    <!-- Letter V as an outline, matching favicon.svg exactly. Kept as a path
         rather than <text> so the mark never depends on a font being present. -->
    <path
      d="M 24,29 L 47,29 L 47,35 L 41,35 L 52,63 L 64,35 L 58,35 L 58,29 L 78,29 L 78,35 L 71,35 L 57,76 L 46,76 L 30,35 L 24,35 Z"
      fill="white"
    />
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
