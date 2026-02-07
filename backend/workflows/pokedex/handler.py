"""
Pokédex Workflow Handler
Entry point que orquestra todo o workflow
"""

from dataclasses import dataclass

from .agent import get_agent
from .config import BLOCKED_MESSAGE
from .guardrails import get_guardrails_service


@dataclass
class PokedexRequest:
    """Request para o workflow Pokédex"""
    pergunta: str
    sessionId: str


@dataclass
class PokedexResponse:
    """Response do workflow Pokédex"""
    output: str
    blocked: bool = False
    error: str | None = None


async def handle_pokedex_request(request: PokedexRequest) -> PokedexResponse:
    """
    Handler principal do workflow Pokédex.

    Fluxo:
    1. Guardrails - verifica jailbreak e alinhamento de tópico
    2. Agent - processa pergunta com RAG + LLM
    3. Response - retorna resposta formatada

    Args:
        request: PokedexRequest com pergunta e sessionId

    Returns:
        PokedexResponse com a resposta ou mensagem de bloqueio
    """
    try:
        # =====================================================================
        # STEP 1: GUARDRAILS CHECK
        # =====================================================================
        guardrails = get_guardrails_service()
        guardrails_result = await guardrails.check(request.pergunta)

        if not guardrails_result.passed:
            # Mensagem bloqueada por guardrails
            return PokedexResponse(
                output=BLOCKED_MESSAGE,
                blocked=True
            )

        # =====================================================================
        # STEP 2: AGENT EXECUTION
        # =====================================================================
        agent = get_agent()
        agent_response = await agent.run(
            question=request.pergunta,
            session_id=request.sessionId,
            include_history=True
        )

        if agent_response.error:
            return PokedexResponse(
                output=agent_response.output,
                error=agent_response.error
            )

        # =====================================================================
        # STEP 3: RETURN RESPONSE
        # =====================================================================
        return PokedexResponse(output=agent_response.output)

    except Exception as e:
        error_msg = f"Workflow error: {str(e)}"
        print(error_msg)
        return PokedexResponse(
            output="Desculpe, ocorreu um erro ao processar sua pergunta. Por favor, tente novamente.",
            error=error_msg
        )


# Função auxiliar para criar request a partir de dict
def create_request_from_dict(data: dict) -> PokedexRequest:
    """
    Cria um PokedexRequest a partir de um dicionário.

    Args:
        data: Dict com 'pergunta' e 'sessionId'

    Returns:
        PokedexRequest
    """
    return PokedexRequest(
        pergunta=data.get("pergunta", ""),
        sessionId=data.get("sessionId", "default")
    )
