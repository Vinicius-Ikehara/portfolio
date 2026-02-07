"""
Vector Store Service
RAG com Supabase pgvector para busca de informações de Pokémon
"""

from dataclasses import dataclass
from typing import List

from openai import OpenAI
from supabase import create_client, Client

from .config import (
    OPENAI_API_KEY,
    POKEDEX_TOOL_DESCRIPTION,
    SUPABASE_POKEDEX_KEY,
    SUPABASE_POKEDEX_URL,
    TOP_K_RESULTS,
    VECTOR_STORE_TABLE,
)


@dataclass
class SearchResult:
    """Resultado de uma busca no vector store"""
    content: str
    metadata: dict
    similarity: float


class VectorStoreService:
    """
    Serviço de vector store usando Supabase pgvector.

    Tabela esperada no Supabase (pokedex_vs):
    - id: bigint primary key
    - content: text
    - metadata: jsonb
    - embedding: vector(1536)

    Função RPC esperada (match_pokedex):
    CREATE OR REPLACE FUNCTION match_pokedex(
        query_embedding vector(1536),
        match_count int DEFAULT 5
    )
    RETURNS TABLE (
        id bigint,
        content text,
        metadata jsonb,
        similarity float
    )
    LANGUAGE plpgsql
    AS $$
    BEGIN
        RETURN QUERY
        SELECT
            pokedex_vs.id,
            pokedex_vs.content,
            pokedex_vs.metadata,
            1 - (pokedex_vs.embedding <=> query_embedding) as similarity
        FROM pokedex_vs
        ORDER BY pokedex_vs.embedding <=> query_embedding
        LIMIT match_count;
    END;
    $$;
    """

    def __init__(self):
        self.supabase: Client = create_client(
            SUPABASE_POKEDEX_URL,
            SUPABASE_POKEDEX_KEY
        )
        self.openai = OpenAI(api_key=OPENAI_API_KEY)
        self.table_name = VECTOR_STORE_TABLE
        self.top_k = TOP_K_RESULTS

    def _get_embedding(self, text: str) -> List[float]:
        """
        Gera embedding para um texto usando OpenAI.

        Args:
            text: Texto para gerar embedding

        Returns:
            Lista de floats representando o embedding
        """
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def search(self, query: str, top_k: int | None = None) -> List[SearchResult]:
        """
        Busca por similaridade no vector store.

        Args:
            query: Texto da busca
            top_k: Número de resultados (default: TOP_K_RESULTS)

        Returns:
            Lista de resultados ordenados por similaridade
        """
        try:
            k = top_k or self.top_k
            print(f"[VectorStore] Searching for: {query}")

            # Gera embedding da query
            query_embedding = self._get_embedding(query)
            print(f"[VectorStore] Embedding generated, length: {len(query_embedding)}")

            # Busca usando função RPC do Supabase
            response = self.supabase.rpc(
                "match_documents",
                {
                    "query_embedding": query_embedding,
                    "match_count": k
                }
            ).execute()

            print(f"[VectorStore] RPC response: {len(response.data) if response.data else 0} results")
            if response.data:
                print(f"[VectorStore] First result: {response.data[0] if response.data else 'None'}")
                return [
                    SearchResult(
                        content=item.get("content", ""),
                        metadata=item.get("metadata", {}),
                        similarity=item.get("similarity", 0.0)
                    )
                    for item in response.data
                ]

            return []

        except Exception as e:
            print(f"Error searching vector store: {e}")
            # Fallback: tenta busca direta na tabela
            return self._fallback_search(query, top_k or self.top_k)

    def _fallback_search(self, query: str, top_k: int) -> List[SearchResult]:
        """
        Busca fallback usando LIKE (menos precisa, mas funciona sem pgvector RPC).
        """
        try:
            # Extrai palavras-chave da query
            keywords = query.lower().split()

            # Busca por conteúdo que contenha as palavras-chave
            response = self.supabase.table(self.table_name).select(
                "content, metadata"
            ).limit(top_k * 2).execute()

            if response.data:
                results = []
                for item in response.data:
                    content = item.get("content", "").lower()
                    # Calcula score simples baseado em matches
                    score = sum(1 for kw in keywords if kw in content) / len(keywords)
                    if score > 0:
                        results.append(SearchResult(
                            content=item.get("content", ""),
                            metadata=item.get("metadata", {}),
                            similarity=score
                        ))

                # Ordena por score e retorna top_k
                results.sort(key=lambda x: x.similarity, reverse=True)
                return results[:top_k]

            return []

        except Exception as e:
            print(f"Error in fallback search: {e}")
            return []

    def format_results_for_llm(self, results: List[SearchResult]) -> str:
        """
        Formata os resultados para uso como contexto no LLM.

        Args:
            results: Lista de resultados da busca

        Returns:
            String formatada com os resultados
        """
        if not results:
            return "Nenhuma informação encontrada na Pokédex."

        formatted_parts = []
        for i, result in enumerate(results, 1):
            # Extrai image_url do metadata se existir
            image_url = result.metadata.get("image_url", "")
            image_info = f"\nImagem: {image_url}" if image_url else ""
            formatted_parts.append(f"[Resultado {i}]\n{result.content}{image_info}")

        return "\n\n".join(formatted_parts)

    def get_tool_definition(self) -> dict:
        """
        Retorna a definição da tool para uso com o LangChain/OpenAI.
        """
        return {
            "type": "function",
            "function": {
                "name": "pokedex",
                "description": POKEDEX_TOOL_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Nome do Pokémon ou pergunta sobre Pokémon para buscar informações"
                        }
                    },
                    "required": ["query"]
                }
            }
        }


# Instância singleton
_vectorstore_service: VectorStoreService | None = None


def get_vectorstore_service() -> VectorStoreService:
    """Retorna a instância singleton do serviço de vector store."""
    global _vectorstore_service
    if _vectorstore_service is None:
        _vectorstore_service = VectorStoreService()
    return _vectorstore_service
