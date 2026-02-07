# Pokédex Workflow
# Migrado do n8n para FastAPI/Python
#
# Componentes:
# - config.py: System prompt, keywords bloqueadas, thresholds
# - guardrails.py: Detecção de jailbreak e validação de tópico
# - memory.py: Histórico de chat por sessão (PostgreSQL)
# - vectorstore.py: RAG com Supabase pgvector
# - agent.py: LangChain Agent com GPT-5.2
# - handler.py: Orquestrador principal (entry point)

from .handler import handle_pokedex_request

__all__ = ["handle_pokedex_request"]
