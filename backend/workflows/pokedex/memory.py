"""
Chat Memory Service
Gerenciamento de histórico de conversa por sessão usando Supabase
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from supabase import create_client, Client

from .config import SUPABASE_POKEDEX_KEY, SUPABASE_POKEDEX_URL


@dataclass
class Message:
    """Representa uma mensagem no histórico"""
    role: str  # "user" ou "assistant"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class ChatHistory:
    """Histórico de uma sessão de chat"""
    session_id: str
    messages: List[Message] = field(default_factory=list)


class ChatMemoryService:
    """
    Serviço de memória de chat usando Supabase.

    Tabela esperada no Supabase:
    - chat_memory (
        id: uuid primary key,
        session_id: text unique,
        messages: jsonb,
        created_at: timestamptz,
        updated_at: timestamptz
      )
    """

    TABLE_NAME = "n8n_chat_histories"

    def __init__(self):
        self.client: Client = create_client(
            SUPABASE_POKEDEX_URL,
            SUPABASE_POKEDEX_KEY
        )

    async def get_history(self, session_id: str, limit: int = 10) -> List[Message]:
        """
        Recupera o histórico de uma sessão.

        Args:
            session_id: ID único da sessão
            limit: Número máximo de mensagens a retornar

        Returns:
            Lista de mensagens ordenadas do mais antigo para o mais recente
        """
        try:
            # Adiciona sufixo "12" ao session_id (como no n8n)
            full_session_id = f"{session_id}12"

            response = self.client.table(self.TABLE_NAME).select("message").eq(
                "session_id", full_session_id
            ).execute()

            if response.data and len(response.data) > 0:
                messages_data = response.data[0].get("message", [])
                messages = [
                    Message(
                        role=msg.get("role", "user"),
                        content=msg.get("content", ""),
                        timestamp=msg.get("timestamp", "")
                    )
                    for msg in messages_data
                ]
                # Retorna as últimas 'limit' mensagens
                return messages[-limit:] if len(messages) > limit else messages

            return []

        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []

    async def add_message(self, session_id: str, role: str, content: str) -> bool:
        """
        Adiciona uma mensagem ao histórico.

        Args:
            session_id: ID único da sessão
            role: "user" ou "assistant"
            content: Conteúdo da mensagem

        Returns:
            True se salvou com sucesso
        """
        try:
            full_session_id = f"{session_id}12"
            new_message = {
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat()
            }

            # Verifica se a sessão já existe
            response = self.client.table(self.TABLE_NAME).select("id, message").eq(
                "session_id", full_session_id
            ).execute()

            if response.data and len(response.data) > 0:
                # Atualiza sessão existente
                existing_messages = response.data[0].get("message", [])
                if existing_messages is None:
                    existing_messages = []
                existing_messages.append(new_message)

                self.client.table(self.TABLE_NAME).update({
                    "message": existing_messages
                }).eq("session_id", full_session_id).execute()
            else:
                # Cria nova sessão
                self.client.table(self.TABLE_NAME).insert({
                    "session_id": full_session_id,
                    "message": [new_message]
                }).execute()

            return True

        except Exception as e:
            print(f"Error adding message to history: {e}")
            return False

    async def add_exchange(
        self,
        session_id: str,
        user_message: str,
        assistant_message: str
    ) -> bool:
        """
        Adiciona uma troca completa (pergunta + resposta) ao histórico.

        Args:
            session_id: ID único da sessão
            user_message: Mensagem do usuário
            assistant_message: Resposta do assistente

        Returns:
            True se salvou com sucesso
        """
        try:
            await self.add_message(session_id, "user", user_message)
            await self.add_message(session_id, "assistant", assistant_message)
            return True
        except Exception as e:
            print(f"Error adding exchange to history: {e}")
            return False

    async def clear_history(self, session_id: str) -> bool:
        """
        Limpa o histórico de uma sessão.

        Args:
            session_id: ID único da sessão

        Returns:
            True se limpou com sucesso
        """
        try:
            full_session_id = f"{session_id}12"
            self.client.table(self.TABLE_NAME).delete().eq(
                "session_id", full_session_id
            ).execute()
            return True
        except Exception as e:
            print(f"Error clearing chat history: {e}")
            return False

    def format_history_for_llm(self, messages: List[Message]) -> List[dict]:
        """
        Formata o histórico para uso com a API do OpenAI.

        Args:
            messages: Lista de mensagens

        Returns:
            Lista de dicts no formato {"role": str, "content": str}
        """
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]


# Instância singleton
_memory_service: ChatMemoryService | None = None


def get_memory_service() -> ChatMemoryService:
    """Retorna a instância singleton do serviço de memória."""
    global _memory_service
    if _memory_service is None:
        _memory_service = ChatMemoryService()
    return _memory_service
