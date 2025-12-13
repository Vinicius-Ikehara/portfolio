<template>
  <div class="pokedex">
    <!-- Top Section -->
    <div class="top-section">
      <div class="camera"></div>
      <div class="leds">
        <div class="led red"></div>
        <div class="led yellow"></div>
        <div class="led green"></div>
      </div>
    </div>

    <!-- Dual Screen Layout -->
    <div class="screens-container">
      <!-- Left Screen: Chat (White) -->
      <div class="screen-left">
        <div class="chat-screen" ref="chatScreen">
          <div v-if="messages.length === 0" class="welcome">
            <span class="welcome-title">Pokédex Online</span><br>
            Ask about any Pokémon!<br><br>
            Examples:<br>
            <div class="example-line">
              <i class="pi pi-bolt"></i> "Tell me about Pikachu"
            </div>
            <div class="example-line">
              <i class="pi pi-sun"></i> "What are Charizard's types?"
            </div>
            <div class="example-line">
              <i class="pi pi-cloud"></i> "How does Squirtle evolve?"
            </div>
          </div>

          <div
            v-for="(msg, index) in messages"
            :key="index"
            :class="['message', msg.type + '-message']"
            v-html="formatMessageText(msg.text)"
          ></div>

          <div v-if="isLoading" class="typing">
            Pokédex is thinking
          </div>
        </div>

        <!-- Controls below chat -->
        <div class="controls">
          <input
            type="text"
            v-model="question"
            @keypress.enter="sendQuestion"
            placeholder="Ask me about any Pokémon..."
            maxlength="200"
            :disabled="isLoading"
          />
          <button @click="sendQuestion" :disabled="isLoading || !question.trim()">
            <i :class="isLoading ? 'pi pi-spin pi-spinner' : 'pi pi-send'"></i>
          </button>
        </div>
      </div>

      <!-- Right Screen: Image Display (Green) -->
      <div class="screen-right">
        <div v-if="currentImage" class="image-display">
          <img :src="currentImage" alt="Pokemon" />
        </div>
        <div v-else class="empty-screen">
          <div class="pokeball-placeholder">
            <svg viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="50" fill="#1a5c1a" opacity="0.3"/>
              <circle cx="50" cy="50" r="35" fill="none" stroke="#0d3d0d" stroke-width="2"/>
              <line x1="15" y1="50" x2="85" y2="50" stroke="#0d3d0d" stroke-width="2"/>
              <circle cx="50" cy="50" r="8" fill="#0d3d0d"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'

const question = ref('')
const messages = ref([])
const isLoading = ref(false)
const chatScreen = ref(null)
const currentImage = ref(null)

const sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const WEBHOOK_URL = `${API_URL}/api/webhook/pokedex`

// Extract image URL from text
const extractImageUrl = (text) => {
  const match = text.match(/\[IMAGEM:\s*(https?:\/\/[^\]]+)\]/)
  return match ? match[1] : null
}

// Format message text (remove image tags, keep only text)
const formatMessageText = (text) => {
  // Remove image tags
  let formatted = text.replace(/\[IMAGEM:\s*https?:\/\/[^\]]+\]/g, '')

  // Converte quebras de linha
  formatted = formatted.replace(/\n/g, '<br>')

  // Remove <br> extras
  formatted = formatted.replace(/(<br>\s*){3,}/g, '<br><br>')

  return formatted.trim()
}

// Watch for new messages and extract image
watch(messages, (newMessages) => {
  if (newMessages.length > 0) {
    const lastMessage = newMessages[newMessages.length - 1]
    if (lastMessage.type === 'bot') {
      const imageUrl = extractImageUrl(lastMessage.text)
      if (imageUrl) {
        currentImage.value = imageUrl
      }
    }
  }
}, { deep: true })

const scrollToBottom = async () => {
  await nextTick()
  if (chatScreen.value) {
    chatScreen.value.scrollTop = chatScreen.value.scrollHeight
  }
}

const sendQuestion = async () => {
  const text = question.value.trim()

  if (!text) return

  if (text.length < 3) {
    messages.value.push({ type: 'system', text: 'Question too short. Be more specific!' })
    scrollToBottom()
    return
  }

  messages.value.push({ type: 'user', text })
  question.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    const response = await fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        pergunta: text,
        sessionId: sessionId
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP Error ${response.status}`)
    }

    const data = await response.json()

    let answer
    if (Array.isArray(data) && data[0] && data[0].output) {
      answer = data[0].output
    } else if (data.resposta) {
      answer = data.resposta
    } else if (data.output) {
      answer = data.output
    } else {
      answer = JSON.stringify(data)
    }

    messages.value.push({ type: 'bot', text: answer })
  } catch (error) {
    console.error('Error:', error)
    messages.value.push({
      type: 'system',
      text: `Error: ${error.message}. Please try again.`
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.pokedex {
  background: linear-gradient(145deg, #dc2626, #b91c1c);
  width: 100%;
  max-width: 1000px;
  border-radius: 20px;
  border: 4px solid #000;
  box-shadow:
    0 20px 40px rgba(0,0,0,0.5),
    inset 0 3px 6px rgba(255,255,255,0.2);
  overflow: hidden;
  margin: 0 auto;
  padding: 20px;
}

/* Top Section */
.top-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.camera {
  width: 50px;
  height: 50px;
  background: radial-gradient(circle at 30% 30%, #22d3ee, #0891b2);
  border-radius: 50%;
  border: 4px solid #000;
  box-shadow:
    0 4px 8px rgba(0,0,0,0.5),
    inset 0 2px 4px rgba(255,255,255,0.4);
  position: relative;
}

.camera::after {
  content: '';
  position: absolute;
  width: 15px;
  height: 15px;
  background: rgba(255,255,255,0.6);
  border-radius: 50%;
  top: 10px;
  left: 12px;
}

.leds {
  display: flex;
  gap: 12px;
}

.led {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 3px solid #000;
  box-shadow:
    0 2px 4px rgba(0,0,0,0.4),
    inset 0 2px 4px rgba(255,255,255,0.5);
}

.led.red { background: radial-gradient(circle at 30% 30%, #ff4444, #cc0000); }
.led.yellow { background: radial-gradient(circle at 30% 30%, #ffff44, #cccc00); }
.led.green { background: radial-gradient(circle at 30% 30%, #44ff44, #00cc00); }

/* Dual Screen Container */
.screens-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  height: 500px;
}

/* Left Screen (White - Chat) */
.screen-left {
  background: #e5e5e5;
  border: 4px solid #000;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: inset 0 4px 8px rgba(0,0,0,0.3);
}

.chat-screen {
  flex: 1;
  background: linear-gradient(145deg, #ffffff, #f5f5f5);
  padding: 15px;
  overflow-y: auto;
  font-size: 14px;
  line-height: 1.5;
}

.controls {
  background: #d4d4d4;
  padding: 12px;
  display: flex;
  gap: 8px;
  border-top: 3px solid #000;
}

.controls input {
  flex: 1;
  padding: 10px 14px;
  border: 2px solid #000;
  border-radius: 20px;
  font-size: 13px;
  outline: none;
  background: #fff;
}

.controls input:focus {
  box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.5);
}

.controls button {
  background: linear-gradient(145deg, #22c55e, #16a34a);
  color: white;
  border: 2px solid #000;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.controls button:hover:not(:disabled) {
  transform: scale(1.05);
  background: linear-gradient(145deg, #16a34a, #15803d);
}

.controls button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* Right Screen (Green - Image) */
.screen-right {
  background: #16a34a;
  border: 4px solid #000;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: inset 0 4px 8px rgba(0,0,0,0.4);
  position: relative;
}

.image-display {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.image-display img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
}

.empty-screen {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pokeball-placeholder {
  width: 120px;
  height: 120px;
  opacity: 0.3;
}

/* Messages */
.message {
  margin-bottom: 8px;
  padding: 8px 12px;
  border-radius: 10px;
  max-width: 90%;
  word-wrap: break-word;
}

.user-message {
  background: #3b82f6;
  color: white;
  margin-left: auto;
  border-bottom-right-radius: 3px;
}

.bot-message {
  background: #f3f4f6;
  color: #1f2937;
  border-bottom-left-radius: 3px;
  margin-right: 0;
}

.system-message {
  background: #fbbf24;
  color: #78350f;
  text-align: center;
  font-size: 12px;
  max-width: 100%;
}

.typing {
  color: #6b7280;
  font-style: italic;
  padding: 8px;
  font-size: 13px;
}

.typing::after {
  content: '...';
  animation: typing-dots 1.5s infinite;
}

@keyframes typing-dots {
  0%, 20% { content: '...'; }
  40% { content: ''; }
  60% { content: '.'; }
  80% { content: '..'; }
  100% { content: '...'; }
}

.welcome {
  text-align: center;
  color: #6b7280;
  font-size: 13px;
  padding: 20px;
}

.welcome-title {
  font-size: 20px;
  font-weight: bold;
  color: #dc2626;
  font-style: normal;
  display: block;
  margin-bottom: 10px;
}

.example-line {
  margin: 6px 0;
  padding: 6px 10px;
  border-radius: 6px;
  background: rgba(59, 130, 246, 0.1);
  font-style: normal;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #374151;
}

/* Responsive */
@media (max-width: 768px) {
  .screens-container {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .screen-right {
    min-height: 300px;
  }

  .pokedex {
    max-width: 100%;
    margin: 0 10px;
    padding: 15px;
  }
}
</style>
