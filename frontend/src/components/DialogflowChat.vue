<template>
  <df-messenger
    agent-id="7bf77edb-587b-4b28-8f40-67b544d24e95"
    language-code="pt-br"
    chat-title="FAQ_BOT_DF"
    intent="WELCOME"
  ></df-messenger>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  // Carrega o script do Dialogflow Messenger se ainda não estiver carregado
  if (!document.querySelector('script[src*="dialogflow"]')) {
    const script = document.createElement('script')
    script.src = 'https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1'
    script.async = true
    document.head.appendChild(script)
  }
})
</script>

<style>
/* Customização do widget flutuante do Dialogflow */
df-messenger {
  --df-messenger-bot-message: #38bdf8;
  --df-messenger-button-titlebar-color: #0284c7;
  --df-messenger-chat-background-color: #ffffff;
  --df-messenger-font-color: #111827;
  --df-messenger-send-icon: #0284c7;
  --df-messenger-user-message: #0284c7;
  z-index: 999;
}
</style>
