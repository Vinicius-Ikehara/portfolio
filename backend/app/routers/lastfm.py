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


@router.get("/newsletter/{data}")
async def newsletter_with_images(
    data: date,
    supabase: Client = Depends(get_supabase),
):
    """Retorna newsletter com imagens dos artistas baseado na data específica"""
    try:
        # 1. Buscar artistas únicos do ranking da data com suas imagens
        rankings_response = (
            supabase.table("rankings_diarios")
            .select("musicas(artista, imagem_url)")
            .eq("data", data.isoformat())
            .order("posicao")
            .execute()
        )

        # 2. Processar para pegar apenas um artista de cada (DISTINCT ON logic)
        artistas_map = {}
        if rankings_response.data:
            for item in rankings_response.data:
                if item.get("musicas"):
                    artista = item["musicas"].get("artista")
                    imagem_url = item["musicas"].get("imagem_url")

                    # Pegar apenas a primeira ocorrência (menor posição) de cada artista
                    if artista and imagem_url and artista not in artistas_map:
                        artistas_map[artista] = imagem_url

        # 3. Buscar newsletter da data específica e adicionar as imagens
        newsletter_response = (
            supabase.table("newsletter")
            .select("*")
            .eq("data", data.isoformat())
            .execute()
        )

        if not newsletter_response.data:
            return []

        # 4. Combinar newsletter com imagens dos artistas
        result = []
        for newsletter_item in newsletter_response.data:
            artista = newsletter_item.get("artista")
            result.append({
                **newsletter_item,
                "imagem_url": artistas_map.get(artista)
            })

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar newsletter: {str(e)}"
        )
