"""Schemas Pydantic para dados do Last.fm"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


# ===== SCHEMAS PARA TABELA 'musicas' =====

class MusicaBase(BaseModel):
    """Schema base para música"""
    track_name: str = Field(..., description="Nome da música")
    artist_name: str = Field(..., description="Nome do artista")
    album_name: Optional[str] = Field(None, description="Nome do álbum")
    duration_ms: Optional[int] = Field(None, description="Duração em milissegundos")
    spotify_id: Optional[str] = Field(None, description="ID do Spotify")
    preview_url: Optional[str] = Field(None, description="URL de preview")
    image_url: Optional[str] = Field(None, description="URL da imagem do álbum")
    genres: Optional[List[str]] = Field(default_factory=list, description="Gêneros musicais")


class MusicaResponse(MusicaBase):
    """Schema de resposta para música"""
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== SCHEMAS PARA TABELA 'rankings_diarios' =====

class RankingDiarioBase(BaseModel):
    """Schema base para ranking diário"""
    data_ranking: date = Field(..., description="Data do ranking")
    musica_id: int = Field(..., description="ID da música")
    posicao: int = Field(..., ge=1, description="Posição no ranking (1+)")
    play_count: int = Field(..., ge=0, description="Número de reproduções")


class RankingDiarioResponse(RankingDiarioBase):
    """Schema de resposta para ranking diário"""
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== SCHEMAS COMBINADOS =====

class RankingComMusica(BaseModel):
    """Ranking combinado com informações da música"""
    data_ranking: date
    posicao: int
    play_count: int
    musica: MusicaResponse


class TopMusicasResponse(BaseModel):
    """Top músicas de um período"""
    periodo: str = Field(..., description="Descrição do período")
    total_musicas: int
    musicas: List[RankingComMusica]


# ===== SCHEMAS PARA INSIGHTS DE IA =====

class InsightRequest(BaseModel):
    """Request para gerar insights"""
    data_inicio: Optional[date] = Field(None, description="Data inicial do período")
    data_fim: Optional[date] = Field(None, description="Data final do período")
    limit: int = Field(10, ge=1, le=100, description="Número de músicas para análise")
    tipo_analise: str = Field(
        "geral",
        description="Tipo de análise: geral, generos, artistas, tendencias"
    )


class InsightResponse(BaseModel):
    """Response com insights gerados pela IA"""
    periodo: str
    total_plays: int
    musicas_analisadas: int
    insights: List[str] = Field(..., description="Lista de insights gerados")
    generos_predominantes: Optional[List[str]] = None
    artistas_destaque: Optional[List[str]] = None
    tendencias: Optional[str] = None


# ===== SCHEMAS PARA ESTATÍSTICAS =====

class EstatisticasGerais(BaseModel):
    """Estatísticas gerais do Last.fm"""
    total_musicas: int
    total_artistas: int
    total_plays: int
    periodo_inicio: Optional[date] = None
    periodo_fim: Optional[date] = None
    media_plays_dia: float
    musica_mais_tocada: Optional[MusicaResponse] = None
