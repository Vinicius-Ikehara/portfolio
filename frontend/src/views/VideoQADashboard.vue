<template>
  <div class="min-h-screen" style="background-color: #111827;">
    <!-- Header -->
    <header class="sticky top-0 z-50 shadow-lg" style="background-color: #0f172a; border-bottom: 1px solid #1e293b;">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <router-link to="/" class="flex items-center gap-2 text-xl font-bold transition-colors" style="color: #38bdf8;">
            <i class="pi pi-arrow-left"></i>
            <span>Back to Portfolio</span>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Project Content -->
    <main class="py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Project Header -->
        <div class="text-center mb-12">
          <div class="flex items-center justify-center gap-3 mb-4">
            <span class="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider" style="background-color: rgba(99, 102, 241, 0.2); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.3);">
              Gemini 2.5 Flash
            </span>
            <span class="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider" style="background-color: rgba(56, 189, 248, 0.2); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.3);">
              Video Upload
            </span>
            <span class="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider" style="background-color: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3);">
              Multimodal AI
            </span>
          </div>
          <h1 class="text-5xl md:text-6xl lg:text-7xl font-bold mb-4" style="color: #ffffff;">
            Video Agent
          </h1>
          <div class="w-24 h-1 mx-auto mb-6" style="background: linear-gradient(90deg, #6366f1, #38bdf8);"></div>
          <p class="text-lg max-w-2xl mx-auto" style="color: #94a3b8;">
            An AI agent that actually watches your videos. Upload a short clip (up to 3 minutes) and ask away —
            powered by <span class="font-semibold" style="color: #a5b4fc;">Gemini 2.5 Flash</span> multimodal analysis.
          </p>
        </div>

        <!-- Phase (a): File Picker -->
        <div v-if="!sessionId" class="max-w-2xl mx-auto">
          <div class="rounded-2xl p-8" style="background-color: #1e293b; border: 1px solid #334155;">
            <div class="flex items-center gap-3 mb-6">
              <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background-color: rgba(99, 102, 241, 0.2);">
                <i class="pi pi-video text-xl" style="color: #a5b4fc;"></i>
              </div>
              <h2 class="text-xl font-bold" style="color: #ffffff;">Upload a video</h2>
            </div>

            <div class="space-y-4">
              <label
                for="video-file-input"
                class="block w-full cursor-pointer rounded-lg text-center py-8 px-4 transition-all"
                :style="fileError
                  ? 'background-color: rgba(239, 68, 68, 0.08); border: 2px dashed #ef4444; color: #fca5a5;'
                  : 'background-color: #0f172a; border: 2px dashed #334155; color: #94a3b8;'"
              >
                <i class="pi pi-cloud-upload text-3xl mb-2 block"></i>
                <span v-if="!selectedFile" class="block text-sm font-medium">Click to choose a video file</span>
                <span v-else class="block text-sm font-medium" style="color: #e2e8f0;">{{ selectedFile.name }}</span>
                <span class="block text-xs mt-1">MP4, MOV, WebM · up to {{ maxSizeMB }}MB · max {{ maxDurationMin }} min</span>
              </label>
              <input
                id="video-file-input"
                ref="fileInput"
                type="file"
                accept="video/*"
                class="hidden"
                @change="onFileSelected"
                aria-label="Selecionar arquivo de vídeo"
              />

              <div v-if="selectedFile && !fileError" class="p-3 rounded-lg text-xs flex items-center gap-3" style="background-color: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.2); color: #7dd3fc;">
                <i class="pi pi-info-circle"></i>
                <span>{{ fileSummary }}</span>
              </div>

              <p v-if="fileError" class="text-sm" style="color: #f87171;">
                <i class="pi pi-exclamation-circle mr-1"></i>{{ fileError }}
              </p>

              <button
                @click="submitUpload"
                :disabled="isSubmitting || !selectedFile || !!fileError"
                class="w-full py-3 px-6 rounded-lg font-semibold text-sm transition-all flex items-center justify-center gap-2"
                style="background-color: #6366f1; color: #ffffff;"
                :class="{ 'opacity-50 cursor-not-allowed': isSubmitting || !selectedFile || !!fileError }"
              >
                <i :class="isSubmitting ? 'pi pi-spin pi-spinner' : 'pi pi-play'"></i>
                {{ isSubmitting ? (uploadProgress ? `Uploading... ${uploadProgress}%` : 'Uploading...') : 'Analyze Video' }}
              </button>
            </div>

            <div class="mt-6 p-4 rounded-lg" style="background-color: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.2);">
              <p class="text-xs font-semibold uppercase tracking-wider mb-2" style="color: #a5b4fc;">How it works</p>
              <ol class="space-y-1 text-sm" style="color: #94a3b8;">
                <li><span class="font-medium" style="color: #cbd5e1;">1.</span> Upload a short video from your device</li>
                <li><span class="font-medium" style="color: #cbd5e1;">2.</span> Gemini watches it (audio + visual fusion)</li>
                <li><span class="font-medium" style="color: #cbd5e1;">3.</span> Ask any question about the content</li>
              </ol>
            </div>
          </div>
        </div>

        <!-- Phase (b): Processing -->
        <div v-else-if="sessionStatus === 'processing'" class="space-y-6">
          <div class="rounded-2xl overflow-hidden" style="border: 1px solid #334155; background-color: #000;">
            <video
              v-if="localVideoUrl"
              :src="localVideoUrl"
              controls
              class="w-full"
              style="max-height: 480px; display: block; margin: 0 auto;"
            ></video>
          </div>

          <div class="rounded-2xl p-8 text-center" style="background-color: #1e293b; border: 1px solid #334155;">
            <i class="pi pi-spin pi-spinner text-4xl mb-4" style="color: #6366f1;"></i>
            <h2 class="text-xl font-bold mb-2" style="color: #ffffff;">Gemini is watching the video...</h2>
            <p class="text-sm" style="color: #94a3b8;">
              Performing audio-visual fusion analysis. This may take a minute.
            </p>
            <div class="mt-4 flex items-center justify-center gap-2 text-xs" style="color: #64748b;">
              <i class="pi pi-clock"></i>
              <span>Polling for completion every 3 seconds</span>
            </div>
          </div>
        </div>

        <!-- Phase (c): Ready -->
        <div v-else-if="sessionStatus === 'ready'" class="space-y-6">
          <div v-if="videoTitle" class="text-center">
            <h2 class="text-2xl font-bold" style="color: #ffffff;">{{ videoTitle }}</h2>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="space-y-4">
              <div class="rounded-2xl overflow-hidden" style="border: 1px solid #334155; background-color: #000;">
                <video
                  ref="videoPlayer"
                  v-if="localVideoUrl"
                  :src="localVideoUrl"
                  controls
                  class="w-full"
                  style="display: block;"
                ></video>
              </div>

              <div class="rounded-xl p-4 flex items-center gap-3" style="background-color: rgba(34, 197, 94, 0.08); border: 1px solid rgba(34, 197, 94, 0.2);">
                <i class="pi pi-check-circle" style="color: #4ade80;"></i>
                <span class="text-sm" style="color: #86efac;">Transcript ready — ask anything about this video</span>
              </div>
            </div>

            <div class="rounded-2xl flex flex-col" style="background-color: #1e293b; border: 1px solid #334155; min-height: 480px;">
              <div class="px-5 py-4 flex items-center gap-3" style="border-bottom: 1px solid #334155;">
                <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background-color: rgba(99, 102, 241, 0.2);">
                  <i class="pi pi-comments" style="color: #a5b4fc;"></i>
                </div>
                <span class="font-semibold text-sm" style="color: #ffffff;">Video Chat</span>
              </div>

              <div
                ref="chatContainer"
                class="flex-1 overflow-y-auto px-5 py-4 space-y-3"
                aria-live="polite"
                aria-label="Chat messages"
                style="max-height: 380px;"
                @click="handleChatClick"
              >
                <div v-if="messages.length === 0" class="text-center py-8" style="color: #64748b;">
                  <i class="pi pi-comments text-3xl mb-3 block"></i>
                  <p class="text-sm">Ask anything about the video content.</p>
                  <p class="text-xs mt-1">Timestamps, concepts, summaries — all fair game.</p>
                </div>

                <div
                  v-for="(msg, index) in messages"
                  :key="index"
                  class="flex"
                  :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
                >
                  <div
                    class="max-w-xs lg:max-w-sm px-4 py-2.5 rounded-2xl text-sm leading-relaxed"
                    :style="msg.role === 'user'
                      ? 'background-color: #6366f1; color: #ffffff; border-bottom-right-radius: 4px;'
                      : 'background-color: #0f172a; color: #e2e8f0; border-bottom-left-radius: 4px; border: 1px solid #334155;'"
                    v-html="formatMessage(msg.content, msg.role === 'user')"
                  ></div>
                </div>

                <div v-if="isChatLoading" class="flex justify-start">
                  <div class="px-4 py-2.5 rounded-2xl text-sm" style="background-color: #0f172a; color: #64748b; border: 1px solid #334155; border-bottom-left-radius: 4px;">
                    <span class="typing-indicator">Thinking</span>
                  </div>
                </div>
              </div>

              <div class="px-5 py-4 flex gap-3" style="border-top: 1px solid #334155;">
                <input
                  v-model="chatInput"
                  type="text"
                  aria-label="Pergunta sobre o vídeo"
                  placeholder="Ask about the video..."
                  maxlength="2000"
                  @keydown.enter="sendMessage"
                  :disabled="isChatLoading"
                  class="flex-1 px-4 py-2.5 rounded-lg text-sm outline-none transition-all"
                  style="background-color: #0f172a; border: 1px solid #334155; color: #e2e8f0;"
                />
                <button
                  @click="sendMessage"
                  :disabled="isChatLoading || !chatInput.trim()"
                  aria-label="Enviar mensagem"
                  class="w-10 h-10 rounded-lg flex items-center justify-center transition-all flex-shrink-0"
                  style="background-color: #6366f1; color: #ffffff;"
                  :class="{ 'opacity-50 cursor-not-allowed': isChatLoading || !chatInput.trim() }"
                >
                  <i :class="isChatLoading ? 'pi pi-spin pi-spinner' : 'pi pi-send'" class="text-sm"></i>
                </button>
              </div>
            </div>
          </div>

          <div class="text-center">
            <button
              @click="resetSession"
              class="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition-all"
              style="background-color: #1e293b; color: #94a3b8; border: 1px solid #334155;"
            >
              <i class="pi pi-refresh"></i>
              Analyze a different video
            </button>
          </div>
        </div>

        <!-- Phase (d): Error -->
        <div v-else-if="sessionStatus === 'error'" class="max-w-2xl mx-auto">
          <div class="rounded-2xl p-8 text-center" style="background-color: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3);">
            <i class="pi pi-exclamation-triangle text-4xl mb-4" style="color: #ef4444;"></i>
            <h2 class="text-xl font-bold mb-2" style="color: #fca5a5;">Transcription Failed</h2>
            <p class="text-sm mb-6" style="color: #94a3b8;">
              {{ errorMessage || 'An error occurred while processing the video. Please try again.' }}
            </p>
            <button
              @click="resetSession"
              class="inline-flex items-center gap-2 px-6 py-3 rounded-lg font-semibold text-sm"
              style="background-color: #dc2626; color: #ffffff;"
            >
              <i class="pi pi-refresh"></i>
              Try Again
            </button>
          </div>
        </div>
      </div>
    </main>

    <footer class="py-8" style="background-color: #030712; color: #9ca3af; border-top: 1px solid #1f2937;">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <router-link
          to="/"
          class="inline-flex items-center gap-2 px-6 py-3 rounded-lg transition-colors font-medium"
          style="background-color: #6366f1; color: #ffffff;"
        >
          <i class="pi pi-arrow-left"></i>
          Back to Portfolio
        </router-link>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount, nextTick } from 'vue'

const API_URL = (typeof window !== 'undefined' && window.APP_CONFIG?.API_URL) || import.meta.env.VITE_API_URL || 'http://localhost:8000'

const MAX_SIZE_BYTES = 100 * 1024 * 1024
const MAX_DURATION_SECONDS = 180
const maxSizeMB = MAX_SIZE_BYTES / (1024 * 1024)
const maxDurationMin = MAX_DURATION_SECONDS / 60

const selectedFile = ref(null)
const selectedDuration = ref(null)
const localVideoUrl = ref(null)
const fileError = ref('')
const isSubmitting = ref(false)
const uploadProgress = ref(0)

const sessionId = ref(null)
const sessionToken = ref(null)
const sessionStatus = ref(null)
const videoTitle = ref(null)
const errorMessage = ref(null)

const messages = ref([])
const chatInput = ref('')
const isChatLoading = ref(false)
const chatContainer = ref(null)
const fileInput = ref(null)
const videoPlayer = ref(null)

let pollingInterval = null

const fileSummary = computed(() => {
  if (!selectedFile.value) return ''
  const sizeMB = (selectedFile.value.size / (1024 * 1024)).toFixed(1)
  if (selectedDuration.value == null) return `${sizeMB}MB`
  const mins = Math.floor(selectedDuration.value / 60)
  const secs = Math.floor(selectedDuration.value % 60)
  return `${mins}min${String(secs).padStart(2, '0')}s · ${sizeMB}MB`
})

function revokeLocalUrl() {
  if (localVideoUrl.value) {
    URL.revokeObjectURL(localVideoUrl.value)
    localVideoUrl.value = null
  }
}

function readDuration(file) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file)
    const probe = document.createElement('video')
    probe.preload = 'metadata'
    probe.onloadedmetadata = () => {
      const dur = probe.duration
      URL.revokeObjectURL(url)
      if (!isFinite(dur)) reject(new Error('Não foi possível ler a duração do vídeo.'))
      else resolve(dur)
    }
    probe.onerror = () => {
      URL.revokeObjectURL(url)
      reject(new Error('Formato de vídeo não suportado pelo browser.'))
    }
    probe.src = url
  })
}

async function onFileSelected(event) {
  fileError.value = ''
  selectedDuration.value = null
  revokeLocalUrl()
  const file = event.target.files?.[0]
  if (!file) {
    selectedFile.value = null
    return
  }

  if (!file.type.startsWith('video/')) {
    fileError.value = 'Arquivo selecionado não é um vídeo.'
    selectedFile.value = null
    return
  }
  if (file.size > MAX_SIZE_BYTES) {
    const mb = (file.size / (1024 * 1024)).toFixed(1)
    fileError.value = `Arquivo tem ${mb}MB. Limite é ${maxSizeMB}MB.`
    selectedFile.value = null
    return
  }

  try {
    const duration = await readDuration(file)
    if (duration > MAX_DURATION_SECONDS) {
      const mins = Math.floor(duration / 60)
      const secs = Math.floor(duration % 60)
      fileError.value = `Vídeo tem ${mins}min${String(secs).padStart(2, '0')}s. Limite é ${maxDurationMin} minutos pra economizar tokens.`
      selectedFile.value = null
      return
    }
    selectedDuration.value = duration
  } catch (err) {
    fileError.value = err.message || 'Não foi possível validar o vídeo.'
    selectedFile.value = null
    return
  }

  selectedFile.value = file
  localVideoUrl.value = URL.createObjectURL(file)
}

function uploadWithProgress(url, formData) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', url)
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) {
        uploadProgress.value = Math.round((e.loaded / e.total) * 100)
      }
    }
    xhr.onload = () => {
      let parsed = null
      try { parsed = JSON.parse(xhr.responseText) } catch { parsed = null }
      resolve({ ok: xhr.status >= 200 && xhr.status < 300, status: xhr.status, data: parsed })
    }
    xhr.onerror = () => reject(new Error('Network error'))
    xhr.send(formData)
  })
}

async function submitUpload() {
  if (isSubmitting.value || !selectedFile.value || fileError.value) return
  isSubmitting.value = true
  uploadProgress.value = 0

  try {
    const formData = new FormData()
    formData.append('video', selectedFile.value)

    const res = await uploadWithProgress(`${API_URL}/api/video-qa/sessions`, formData)

    if (!res.ok) {
      fileError.value = res.data?.detail || `Server error: ${res.status}`
      return
    }

    sessionId.value = res.data.id
    sessionToken.value = res.data.session_token
    sessionStatus.value = res.data.status
    startPolling()
  } catch {
    fileError.value = 'Falha ao conectar ao servidor. Tente novamente.'
  } finally {
    isSubmitting.value = false
    uploadProgress.value = 0
  }
}

function startPolling() {
  stopPolling()
  pollingInterval = setInterval(pollStatus, 3000)
}

function stopPolling() {
  if (pollingInterval) {
    clearInterval(pollingInterval)
    pollingInterval = null
  }
}

async function pollStatus() {
  if (!sessionId.value || !sessionToken.value) return
  try {
    const res = await fetch(`${API_URL}/api/video-qa/sessions/${sessionId.value}`, {
      headers: { 'X-Session-Token': sessionToken.value },
    })
    if (!res.ok) return
    const data = await res.json()
    sessionStatus.value = data.status
    videoTitle.value = data.video_title || null
    errorMessage.value = data.error_message || null

    if (data.status === 'ready' || data.status === 'error') {
      stopPolling()
    }
  } catch {
    // silently ignore polling errors
  }
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function formatMessage(content, isUser) {
  if (isUser) {
    return escapeHtml(content).replace(/\n/g, '<br>')
  }

  let html = escapeHtml(content)

  // Bold: **text**
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')

  // Timestamps [MM:SS] → clickable chip
  html = html.replace(/\[(\d{1,2}):(\d{2})\]/g, (_, mm, ss) => {
    const secs = parseInt(mm) * 60 + parseInt(ss)
    return `<span class="ts-link" data-seconds="${secs}" title="Jump to ${mm}:${ss} in video">${mm}:${ss}</span>`
  })

  // Process lines: detect bullet/numbered lists, convert the rest to <br>
  const lines = html.split('\n')
  const result = []
  let listTag = null

  for (const line of lines) {
    const bulletMatch = line.match(/^[-*•]\s+(.+)/)
    const numberedMatch = line.match(/^\d+\.\s+(.+)/)

    if (bulletMatch) {
      if (listTag !== 'ul') {
        if (listTag) result.push(`</${listTag}>`)
        result.push('<ul>')
        listTag = 'ul'
      }
      result.push(`<li>${bulletMatch[1]}</li>`)
    } else if (numberedMatch) {
      if (listTag !== 'ol') {
        if (listTag) result.push(`</${listTag}>`)
        result.push('<ol>')
        listTag = 'ol'
      }
      result.push(`<li>${numberedMatch[1]}</li>`)
    } else {
      if (listTag) { result.push(`</${listTag}>`); listTag = null }
      result.push(line === '' ? '<br>' : line + '<br>')
    }
  }

  if (listTag) result.push(`</${listTag}>`)

  return result.join('').replace(/(<br>)+$/, '')
}

function handleChatClick(event) {
  const el = event.target.closest('.ts-link')
  if (!el || !videoPlayer.value) return
  const seconds = parseFloat(el.dataset.seconds)
  if (isNaN(seconds)) return
  videoPlayer.value.currentTime = seconds
  videoPlayer.value.play().catch(() => {})
}

async function sendMessage() {
  const text = chatInput.value.trim()
  if (!text || isChatLoading.value) return

  messages.value.push({ role: 'user', content: text })
  chatInput.value = ''
  isChatLoading.value = true
  await scrollToBottom()

  try {
    const historyToSend = messages.value
      .slice(0, -1)
      .slice(-20)
      .map(m => ({ role: m.role, content: m.content }))

    const res = await fetch(`${API_URL}/api/video-qa/sessions/${sessionId.value}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Session-Token': sessionToken.value || '',
      },
      body: JSON.stringify({ pergunta: text, history: historyToSend }),
    })

    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      messages.value.push({ role: 'assistant', content: data.detail || 'Error generating response.' })
    } else {
      const data = await res.json()
      messages.value.push({ role: 'assistant', content: data.resposta ?? 'Sem resposta recebida.' })
    }
  } catch {
    messages.value.push({ role: 'assistant', content: 'Network error. Please try again.' })
  } finally {
    isChatLoading.value = false
    await scrollToBottom()
  }
}

async function scrollToBottom() {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

function resetSession() {
  stopPolling()
  revokeLocalUrl()
  sessionId.value = null
  sessionToken.value = null
  sessionStatus.value = null
  videoTitle.value = null
  errorMessage.value = null
  messages.value = []
  chatInput.value = ''
  selectedFile.value = null
  selectedDuration.value = null
  fileError.value = ''
  uploadProgress.value = 0
  if (fileInput.value) fileInput.value.value = ''
}

onBeforeUnmount(() => {
  stopPolling()
  revokeLocalUrl()
})
</script>

<style scoped>
.typing-indicator::after {
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

input::placeholder {
  color: #475569;
}

:deep(.ts-link) {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  background-color: rgba(99, 102, 241, 0.18);
  color: #a5b4fc;
  border: 1px solid rgba(99, 102, 241, 0.4);
  border-radius: 4px;
  padding: 0 5px;
  font-size: 0.75rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  cursor: pointer;
  transition: background-color 0.15s, color 0.15s;
}

:deep(.ts-link::before) {
  content: '▶';
  font-size: 0.6rem;
}

:deep(.ts-link:hover) {
  background-color: rgba(99, 102, 241, 0.35);
  color: #c7d2fe;
}

:deep(ul), :deep(ol) {
  margin: 4px 0;
  padding-left: 1.25rem;
}

:deep(ul) {
  list-style-type: disc;
}

:deep(ol) {
  list-style-type: decimal;
}

:deep(li) {
  margin: 2px 0;
}

input:focus, label:hover {
  border-color: #6366f1 !important;
}
</style>
