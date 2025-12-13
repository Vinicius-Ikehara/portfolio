<template>
  <div class="pokedex">
    <div class="top-section">
      <div class="camera"></div>
      <div class="leds">
        <div class="led red"></div>
        <div class="led yellow"></div>
        <div class="led green"></div>
      </div>
    </div>

    <div class="screen" ref="chatScreen">
      <!-- Spinning Pokeball background -->
      <svg class="pokeball-bg" viewBox="0 0 512 512">
        <circle cx="256" cy="256" r="256" fill="#FF6B6B"/>
        <path d="M256 0C145.929 0 52.094 69.472 15.923 166.957h480.154C459.906 69.472 366.071 0 256 0z" fill="#E85A5A"/>
        <circle cx="256" cy="256" r="256" fill="#FFFFFF" style="clip-path: polygon(0 50%, 100% 50%, 100% 100%, 0 100%)"/>
        <path d="M256 512c110.071 0 203.906-69.472 240.077-166.957H15.923C52.094 442.528 145.929 512 256 512z" fill="#E5E5E5"/>
        <rect x="0" y="230" width="512" height="52" fill="#4A5568"/>
        <circle cx="256" cy="256" r="75" fill="#4A5568"/>
        <circle cx="256" cy="256" r="45" fill="#E5E5E5"/>
        <circle cx="256" cy="256" r="35" fill="#FFFFFF"/>
      </svg>

      <div v-if="messages.length === 0" class="welcome">
        <span class="welcome-title">Pokédex Online</span><br>
        Ask about any Pokémon!<br><br>
        Examples:<br>
        <div class="example-line electric">
          <i class="pi pi-bolt"></i> "Tell me about Pikachu"
        </div>
        <div class="example-line fire">
          <i class="pi pi-sun"></i> "What are Charizard's types?"
        </div>
        <div class="example-line water">
          <i class="pi pi-cloud"></i> "How does Squirtle evolve?"
        </div>
      </div>

      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.type + '-message']"
        v-html="formatMessage(msg.text)"
      ></div>

      <div v-if="isLoading" class="typing">
        Pokédex is thinking
      </div>
    </div>

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
</template>

<script setup>
import { ref, nextTick } from 'vue'

const question = ref('')
const messages = ref([])
const isLoading = ref(false)
const chatScreen = ref(null)

const sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const WEBHOOK_URL = `${API_URL}/api/webhook/pokedex`

const formatMessage = (text) => {
  // Converte markdown de imagens para HTML
  let formatted = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" class="pokemon-image" />')

  // Converte quebras de linha para <br>
  formatted = formatted.replace(/\n/g, '<br>')

  return formatted
}

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
  background: linear-gradient(145deg, #ff2e2e, #d32f2f);
  width: 100%;
  max-width: 750px;
  border-radius: 20px;
  border: 4px solid #000;
  box-shadow:
    0 15px 30px rgba(0,0,0,0.4),
    inset 0 3px 6px rgba(255,255,255,0.2),
    inset 0 -3px 6px rgba(0,0,0,0.3);
  overflow: hidden;
  margin: 0 auto;
}

.top-section {
  background: linear-gradient(145deg, #ff2e2e, #d32f2f);
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: inset 0 2px 4px rgba(255,255,255,0.1);
}

.camera {
  width: 25px;
  height: 25px;
  background: linear-gradient(145deg, cyan, #17a2b8);
  border-radius: 50%;
  border: 3px solid #000;
  box-shadow:
    0 3px 6px rgba(0,0,0,0.4),
    inset 0 1px 2px rgba(255,255,255,0.3),
    inset 0 -1px 2px rgba(0,0,0,0.3);
}

.leds {
  display: flex;
  gap: 8px;
}

.led {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  border: 2px solid #000;
  box-shadow:
    0 2px 4px rgba(0,0,0,0.3),
    inset 0 1px 2px rgba(255,255,255,0.4),
    inset 0 -1px 1px rgba(0,0,0,0.2);
}

.led.red { background: linear-gradient(145deg, #ff0000, #cc0000); }
.led.yellow { background: linear-gradient(145deg, #ffff00, #cccc00); }
.led.green { background: linear-gradient(145deg, #00ff00, #00cc00); }

.screen {
  background: linear-gradient(145deg, #fff, #f8f9fa);
  margin: 0 15px;
  border: 3px solid #000;
  border-radius: 10px;
  height: 450px;
  padding: 15px;
  overflow-y: auto;
  font-size: 16px;
  line-height: 1.6;
  position: relative;
  box-shadow:
    inset 0 3px 6px rgba(0,0,0,0.2),
    inset 0 -1px 3px rgba(255,255,255,0.3);
}

.controls {
  background: linear-gradient(145deg, cyan, #17a2b8);
  padding: 15px;
  display: flex;
  gap: 10px;
  align-items: center;
  box-shadow:
    inset 0 2px 4px rgba(255,255,255,0.2),
    inset 0 -2px 4px rgba(0,0,0,0.2);
}

.controls input {
  flex: 1;
  padding: 12px 16px;
  border: 3px solid #000;
  border-radius: 25px;
  font-size: 14px;
  outline: none;
  background: linear-gradient(145deg, #fff, #f8f9fa);
  box-shadow:
    inset 0 2px 4px rgba(0,0,0,0.2),
    0 1px 2px rgba(255,255,255,0.3);
  transition: all 0.3s ease;
}

.controls input:focus {
  box-shadow:
    inset 0 2px 6px rgba(0,0,0,0.3),
    0 0 0 3px rgba(46, 204, 113, 0.3);
}

.controls input::placeholder {
  color: #95a5a6;
  font-style: italic;
}

.controls button {
  background: linear-gradient(145deg, #2ecc71, #27ae60);
  color: white;
  border: 3px solid #000;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 4px 8px rgba(0,0,0,0.3),
    inset 0 2px 4px rgba(255,255,255,0.3),
    inset 0 -2px 4px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
}

.controls button:hover:not(:disabled) {
  background: linear-gradient(145deg, #27ae60, #229954);
  transform: scale(1.1);
}

.controls button:disabled {
  background: linear-gradient(145deg, #6c757d, #495057);
  cursor: not-allowed;
  transform: none;
}

.message {
  margin-bottom: 10px;
  padding: 10px 14px;
  border-radius: 12px;
  position: relative;
  z-index: 2;
}

.user-message {
  background: #3498db;
  color: white;
  margin-left: 40px;
  border-bottom-right-radius: 4px;
}

.bot-message {
  background: #ecf0f1;
  color: #2c3e50;
  margin-right: 40px;
  border-bottom-left-radius: 4px;
}

.system-message {
  background: #f39c12;
  color: white;
  text-align: center;
  font-size: 14px;
}

.typing {
  position: relative;
  z-index: 2;
  color: #7f8c8d;
  font-style: italic;
  padding: 8px;
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
  color: #7f8c8d;
  font-style: italic;
  position: relative;
  z-index: 2;
  padding: 20px;
}

.welcome-title {
  font-size: 24px;
  font-weight: bold;
  color: #e74c3c;
  font-style: normal;
}

.example-line {
  margin: 8px 0;
  padding: 8px 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);
  font-style: normal;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 8px;
}

.electric { color: #f1c40f; }
.fire { color: #e74c3c; }
.water { color: #3498db; }

.pokeball-bg {
  position: absolute;
  width: 250px;
  height: 250px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.06;
  pointer-events: none;
  animation: spin 15s linear infinite;
  z-index: 1;
}

@keyframes spin {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

.pokemon-image {
  max-width: 200px;
  width: 100%;
  height: auto;
  border-radius: 12px;
  margin: 10px 0;
  display: block;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  background: white;
  border: 3px solid #000;
}

.bot-message .pokemon-image {
  margin-left: 0;
}

.user-message .pokemon-image {
  margin-left: auto;
}
</style>
