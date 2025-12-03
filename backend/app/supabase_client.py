"""Cliente Supabase para acesso ao banco de dados Last.fm"""
from supabase import create_client, Client
from app.config import settings


class SupabaseClient:
    """Singleton para cliente Supabase"""
    _instance: Client = None

    @classmethod
    def get_client(cls) -> Client:
        """Retorna instância do cliente Supabase"""
        if cls._instance is None:
            if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
                raise ValueError(
                    "SUPABASE_URL e SUPABASE_KEY devem ser configurados no .env"
                )
            cls._instance = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return cls._instance


def get_supabase() -> Client:
    """Dependency para injeção do cliente Supabase"""
    return SupabaseClient.get_client()
