"""Router para endpoints do Last.fm"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import date
from supabase import Client

from app.supabase_client import get_supabase

router = APIRouter(prefix="/lastfm", tags=["Last.fm"])


@router.get("/ranking/latest")
async def ranking_latest(
    supabase: Client = Depends(get_supabase),
):
    """Retorna o top 10 músicas da data mais recente disponível"""
    try:
        # Buscar a data mais recente
        latest_date_response = (
            supabase.table("rankings_diarios")
            .select("data")
            .order("data", desc=True)
            .limit(1)
            .execute()
        )

        if not latest_date_response.data:
            raise HTTPException(
                status_code=404,
                detail="Nenhum ranking encontrado no banco de dados"
            )

        latest_date = latest_date_response.data[0]["data"]

        # Buscar os 10 primeiros rankings dessa data com informações das músicas
        response = (
            supabase.table("rankings_diarios")
            .select("*, musicas(*)")
            .eq("data", latest_date)
            .order("posicao")
            .limit(10)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail=f"Nenhum ranking encontrado para a data {latest_date}"
            )

        return response.data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar ranking: {str(e)}"
        )


@router.get("/ranking/{data}")
async def ranking_top10(
    data: date,
    supabase: Client = Depends(get_supabase),
):
    """Retorna o top 10 músicas de uma data específica com variação de posição"""
    try:
        # Buscar os 10 primeiros rankings da data com informações das músicas
        response = (
            supabase.table("rankings_diarios")
            .select("*, musicas(*)")
            .eq("data", data.isoformat())
            .order("posicao")
            .limit(10)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail=f"Nenhum ranking encontrado para a data {data}"
            )

        return response.data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar ranking: {str(e)}"
        )
