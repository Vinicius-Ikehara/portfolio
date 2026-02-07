"""
Pokédex AI Agent
Agente principal usando Agno + GPT + RAG

Agno é um framework moderno para construir agentes de IA.
Documentação: https://docs.agno.com
"""

from dataclasses import dataclass
from typing import List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool

from .config import (
    LLM_TEMPERATURE,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    SYSTEM_PROMPT,
)
from .memory import get_memory_service
from .vectorstore import get_vectorstore_service


@dataclass
class AgentResponse:
    """Resposta do agente"""
    output: str
    tool_calls: List[dict] | None = None
    error: str | None = None


# =============================================================================
# TOOLS DEFINITION
# =============================================================================

@tool
def pokedex(query: str) -> str:
    """Base de dados com informações dos Pokémon da primeira geração (Kanto).

    Use esta ferramenta para buscar informações sobre qualquer Pokémon,
    incluindo stats, tipos, evoluções, habilidades e fraquezas.

    Args:
        query: Nome do Pokémon ou pergunta sobre Pokémon

    Returns:
        Informações encontradas sobre o Pokémon
    """
    vectorstore = get_vectorstore_service()
    results = vectorstore.search(query)
    return vectorstore.format_results_for_llm(results)


class PokedexAgent:
    """
    Agente Pokédex usando Agno.

    Fluxo:
    1. Recebe pergunta do usuário
    2. Busca histórico da sessão
    3. Usa Agno agent com tool calling
    4. Gera resposta formatada
    5. Salva no histórico
    """

    def __init__(self):
        # Modelo OpenAI via Agno
        self.model = OpenAIChat(
            id=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=LLM_TEMPERATURE
        )

        # Cria agente Agno com tools
        self.agent = Agent(
            model=self.model,
            tools=[pokedex],
            instructions=SYSTEM_PROMPT,
            markdown=True
        )

        # Memory service
        self.memory = get_memory_service()

    async def run(
        self,
        question: str,
        session_id: str,
        include_history: bool = True
    ) -> AgentResponse:
        """
        Executa o agente para responder uma pergunta.

        Args:
            question: Pergunta do usuário
            session_id: ID da sessão para histórico
            include_history: Se deve incluir histórico da conversa

        Returns:
            AgentResponse com a resposta
        """
        try:
            # 1. Busca histórico se habilitado
            history_context = ""
            if include_history:
                history = await self.memory.get_history(session_id, limit=10)
                if history:
                    history_lines = []
                    for msg in history:
                        role = "Usuário" if msg.role == "user" else "Pokédex"
                        history_lines.append(f"{role}: {msg.content}")
                    history_context = "\n\nHistórico da conversa:\n" + "\n".join(history_lines) + "\n\n"

            # 2. Monta prompt com histórico
            full_prompt = f"{history_context}Pergunta atual: {question}"

            # 3. Executa agente
            response = self.agent.run(full_prompt)

            # 4. Extrai resposta
            final_response = response.content if hasattr(response, 'content') else str(response)

            # 5. Extrai tool calls (se disponível)
            tool_calls_made = []
            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tc in response.tool_calls:
                    tool_calls_made.append({
                        "name": getattr(tc, 'name', 'pokedex'),
                        "arguments": getattr(tc, 'arguments', {})
                    })

            # 6. Salva no histórico
            await self.memory.add_exchange(session_id, question, final_response)

            return AgentResponse(
                output=final_response,
                tool_calls=tool_calls_made if tool_calls_made else None
            )

        except Exception as e:
            error_msg = f"Erro ao processar pergunta: {str(e)}"
            print(error_msg)
            return AgentResponse(
                output="Desculpe, ocorreu um erro ao processar sua pergunta. Por favor, tente novamente.",
                error=error_msg
            )


# Instância singleton
_agent: PokedexAgent | None = None


def get_agent() -> PokedexAgent:
    """Retorna a instância singleton do agente."""
    global _agent
    if _agent is None:
        _agent = PokedexAgent()
    return _agent
