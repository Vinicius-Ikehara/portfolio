<template>
  <df-messenger
    agent-id="7bf77edb-587b-4b28-8f40-67b544d24e95"
    language-code="en"
    chat-title="Virtual Assistant"
    intent="WELCOME"
  ></df-messenger>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  if (!document.querySelector('script[src*="dialogflow"]')) {
    const script = document.createElement('script')
    script.src = 'https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1'
    script.async = true
    document.head.appendChild(script)
  }
})
</script>

<style>
df-messenger {
  --df-messenger-bot-message: #dbeafe;
  --df-messenger-button-titlebar-color: #38bdf8;
  --df-messenger-chat-background-color: #ffffff;
  --df-messenger-font-color: #1f2937;
  --df-messenger-send-icon: #38bdf8;
  --df-messenger-user-message: #bfdbfe;
  z-index: 999;
}

/* Customiza o ícone do botão flutuante */
df-messenger::part(chat-bubble-button-icon) {
  background-image: url('data:image/svg+xml;charset=UTF-8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/><circle cx="8" cy="10" r="1.5"/><circle cx="12" cy="10" r="1.5"/><circle cx="16" cy="10" r="1.5"/></svg>') !important;
  background-size: 60%;
  background-repeat: no-repeat;
  background-position: center;
}

df-messenger::part(chat-bubble-button-icon) svg {
  display: none;
}
</style>
