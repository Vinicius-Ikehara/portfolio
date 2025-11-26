<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <router-view />
    <DialogflowChat />
  </div>
</template>

<script setup>
import DialogflowChat from './components/DialogflowChat.vue'
</script>

<style scoped>
</style>
