# Pokédex Workflow - Documentação Técnica

Chatbot AI nativo em Python usando Agno framework + RAG com Supabase pgvector.

## Estrutura

```
backend/workflows/pokedex/
├── __init__.py           # Exports handler
├── config.py             # System prompt, keywords, thresholds
├── guardrails.py         # Jailbreak + topic detection
├── memory.py             # Chat history (Supabase)
├── vectorstore.py        # RAG com pgvector
├── agent.py              # Agno Agent + GPT-5.2
└── handler.py            # Orquestrador (entry point)
```

## Fluxo

```
POST /api/webhook/pokedex
         │
         ▼
    ┌─────────────┐
    │  Guardrails │ ─── Blocked? ──▶ {"output": "Message blocked..."}
    └─────────────┘
         │ Pass
         ▼
    ┌─────────────┐
    │    Agent    │
    │   (Agno)    │
    │      │      │
    │      ├── Memory (histórico)
    │      ├── VectorStore (RAG)
    │      └── LLM (GPT-5.2)
    └─────────────┘
         │
         ▼
    {"output": "Resposta formatada..."}
```

## Componentes

### 1. Guardrails (`guardrails.py`)

Proteção contra jailbreak e off-topic:

- **Keywords bloqueadas**: "ignore", "jailbreak", "prompt injection", etc.
- **Padrões suspeitos**: `[INST]`, `###system`, tentativas de injeção
- **Análise de tópico**: Verifica se é sobre Pokémon Gen 1 (usa LLM)

**Thresholds:**
- Jailbreak: 0.6
- Topic alignment: 0.7

### 2. Memory (`memory.py`)

Histórico de chat por sessão usando Supabase:

**Tabela: `n8n_chat_histories`**
```sql
-- Estrutura existente no Supabase
-- Coluna principal: message (JSONB array)
-- Session ID com sufixo "12" para compatibilidade
```

### 3. VectorStore (`vectorstore.py`)

RAG usando Supabase pgvector:

**Embedding Model**: `text-embedding-3-small` (OpenAI)

**Função RPC**: `match_documents`
- Recebe: `query_embedding` (vector 1536), `match_count` (int)
- Retorna: `id`, `content`, `metadata` (com `image_url`), `similarity`

**Formato do resultado para LLM**:
```
[Resultado 1]
Pikachu (#025) é um Pokémon do tipo Elétrico...
Imagem: https://storage.supabase.co/pokemons/025.png
```

### 4. Agent (`agent.py`)

Agente usando Agno framework:

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-5.2"),
    tools=[pokedex],
    instructions=SYSTEM_PROMPT,
    markdown=True
)
```

**Tool `pokedex`**: Busca no vector store e retorna informações formatadas com URL da imagem.

### 5. Handler (`handler.py`)

Entry point que orquestra todo o fluxo:

```python
async def handle_pokedex_request(request: PokedexRequest) -> PokedexResponse:
    # 1. Guardrails check
    # 2. Agent execution
    # 3. Return response
```

## Variáveis de Ambiente

```env
# Supabase Pokédex
SUPABASE_POKEDEX_URL=https://xxx.supabase.co
SUPABASE_POKEDEX_KEY=eyJ...

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5.2
```

## System Prompt

O system prompt define o comportamento do Pokédex (ver `config.py`):

- Responde no mesmo idioma da pergunta
- Usa a tool `pokedex` para buscar dados
- Formata respostas com emojis e markdown
- Mostra imagem do Pokémon: `[IMAGEM: url-real]`
- Apenas Pokémon Gen 1 (Kanto)

## Formato de Imagem

O frontend (`PokedexChat.vue`) espera:
```
[IMAGEM: https://url-completa-da-imagem.png]
```

O componente extrai a URL via regex e exibe na tela verde da Pokédex.

## Dependências

```txt
agno>=1.0.0
openai>=1.10.0
supabase>=2.10.0
```

## Testando

```bash
curl -X POST http://localhost:8000/api/webhook/pokedex \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Me fale sobre o Pikachu", "sessionId": "test123"}'
```
