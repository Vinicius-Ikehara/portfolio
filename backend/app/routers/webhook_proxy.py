from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/webhook", tags=["webhook"])


class PokedexRequest(BaseModel):
    pergunta: str
    sessionId: str


@router.post("/pokedex")
async def pokedex_chat(request: PokedexRequest):
    """
    Endpoint para o chatbot Pokédex.

    Usa o workflow local Python/Agno com:
    - Guardrails (jailbreak + topic detection)
    - RAG com Supabase pgvector
    - Agent Agno + GPT-5.2
    - Memory por sessão
    """
    try:
        from workflows.pokedex import handle_pokedex_request
        from workflows.pokedex.handler import PokedexRequest as WorkflowRequest

        # Cria request para o workflow
        workflow_request = WorkflowRequest(
            pergunta=request.pergunta,
            sessionId=request.sessionId
        )

        # Executa workflow
        response = await handle_pokedex_request(workflow_request)

        # Retorna resposta
        return {"output": response.output}

    except Exception as e:
        print(f"Workflow error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Desculpe, ocorreu um erro ao processar sua pergunta. Por favor, tente novamente."
        )
