import time
from typing import Any

from fastapi import APIRouter, HTTPException

from ..config import settings

router = APIRouter(tags=["acidentes-h3"])

# Simple in-memory cache with TTL
_cache: dict[str, Any] = {}
_CACHE_TTL = 300  # 5 minutes


def _is_cache_valid(key: str) -> bool:
    entry = _cache.get(key)
    return entry is not None and (time.time() - entry["timestamp"]) < _CACHE_TTL


def _get_client():
    """Get ClickHouse HTTP client using httpx."""
    import httpx
    return httpx.Client(
        base_url=settings.CLICKHOUSE_URL,
        timeout=30.0,
    )


def _query_clickhouse(query: str) -> list[dict]:
    """Execute a ClickHouse query and return rows as dicts."""
    import httpx
    response = httpx.post(
        settings.CLICKHOUSE_URL,
        content=query + " FORMAT JSON",
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("data", [])


@router.get("/acidentes/summary")
async def get_summary():
    """Summary metrics: total accidents, deaths, injuries."""
    cache_key = "summary"
    if _is_cache_valid(cache_key):
        return _cache[cache_key]["data"]

    try:
        rows = _query_clickhouse("""
            SELECT
                countDistinct(id) as total_acidentes,
                count() as total_envolvidos,
                sum(mortos) as total_mortos,
                sum(feridos_graves) as total_feridos_graves,
                sum(feridos_leves) as total_feridos_leves,
                min(data_inversa) as data_inicio,
                max(data_inversa) as data_fim
            FROM acidentes.ocorrencias
        """)
        result = rows[0] if rows else {}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"ClickHouse error: {e}")

    _cache[cache_key] = {"data": result, "timestamp": time.time()}
    return result


@router.get("/acidentes/h3-hexagons")
async def get_h3_hexagons(metric: str = "acidentes"):
    """H3 hexagons aggregated data for map visualization."""
    cache_key = f"h3_{metric}"
    if _is_cache_valid(cache_key):
        return _cache[cache_key]["data"]

    if metric == "mortos":
        value_col = "sum(mortos) as value"
    elif metric == "feridos":
        value_col = "sum(feridos_graves) + sum(feridos_leves) as value"
    elif metric == "letalidade":
        value_col = "round(sum(mortos) * 100.0 / countDistinct(id), 2) as value"
    else:
        value_col = "countDistinct(id) as value"

    try:
        rows = _query_clickhouse(f"""
            SELECT
                h3ToString(h3_index) as h3_index,
                {value_col},
                countDistinct(id) as acidentes,
                sum(mortos) as mortos,
                any(municipio) as municipio,
                any(uf) as uf,
                any(concat('BR-', toString(br))) as rodovia
            FROM acidentes.ocorrencias
            WHERE h3_index > 0
            GROUP BY h3_index
            HAVING countDistinct(id) >= 2
            ORDER BY value DESC
        """)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"ClickHouse error: {e}")

    _cache[cache_key] = {"data": rows, "timestamp": time.time()}
    return rows


@router.get("/acidentes/by-state")
async def get_by_state():
    """Accidents aggregated by state."""
    cache_key = "by_state"
    if _is_cache_valid(cache_key):
        return _cache[cache_key]["data"]

    try:
        rows = _query_clickhouse("""
            SELECT
                uf,
                countDistinct(id) as total_acidentes,
                sum(mortos) as total_mortos,
                sum(feridos_graves) as total_feridos_graves,
                round(sum(mortos) * 100.0 / countDistinct(id), 2) as taxa_letalidade
            FROM acidentes.ocorrencias
            GROUP BY uf
            ORDER BY total_acidentes DESC
        """)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"ClickHouse error: {e}")

    _cache[cache_key] = {"data": rows, "timestamp": time.time()}
    return rows


@router.get("/acidentes/by-cause")
async def get_by_cause():
    """Top accident causes with lethality rate."""
    cache_key = "by_cause"
    if _is_cache_valid(cache_key):
        return _cache[cache_key]["data"]

    try:
        rows = _query_clickhouse("""
            SELECT
                causa_acidente,
                countDistinct(id) as total_acidentes,
                sum(mortos) as total_mortos,
                round(sum(mortos) * 100.0 / countDistinct(id), 2) as taxa_letalidade
            FROM acidentes.ocorrencias
            GROUP BY causa_acidente
            ORDER BY total_acidentes DESC
            LIMIT 10
        """)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"ClickHouse error: {e}")

    _cache[cache_key] = {"data": rows, "timestamp": time.time()}
    return rows


@router.get("/acidentes/by-hour")
async def get_by_hour():
    """Accidents by hour of day."""
    cache_key = "by_hour"
    if _is_cache_valid(cache_key):
        return _cache[cache_key]["data"]

    try:
        rows = _query_clickhouse("""
            SELECT
                substring(horario, 1, 2) as hora,
                countDistinct(id) as total_acidentes,
                sum(mortos) as total_mortos
            FROM acidentes.ocorrencias
            GROUP BY hora
            ORDER BY hora
        """)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"ClickHouse error: {e}")

    _cache[cache_key] = {"data": rows, "timestamp": time.time()}
    return rows


@router.get("/acidentes/by-highway")
async def get_by_highway():
    """Most dangerous highways."""
    cache_key = "by_highway"
    if _is_cache_valid(cache_key):
        return _cache[cache_key]["data"]

    try:
        rows = _query_clickhouse("""
            SELECT
                concat('BR-', toString(br)) as rodovia,
                uf,
                countDistinct(id) as total_acidentes,
                sum(mortos) as total_mortos,
                round(sum(mortos) * 100.0 / countDistinct(id), 2) as taxa_letalidade
            FROM acidentes.ocorrencias
            GROUP BY br, uf
            ORDER BY total_acidentes DESC
            LIMIT 15
        """)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"ClickHouse error: {e}")

    _cache[cache_key] = {"data": rows, "timestamp": time.time()}
    return rows


@router.get("/acidentes/by-day-of-week")
async def get_by_day_of_week():
    """Accidents by day of week."""
    cache_key = "by_dow"
    if _is_cache_valid(cache_key):
        return _cache[cache_key]["data"]

    try:
        rows = _query_clickhouse("""
            SELECT
                dia_semana,
                countDistinct(id) as total_acidentes,
                sum(mortos) as total_mortos,
                round(sum(mortos) * 100.0 / countDistinct(id), 2) as taxa_letalidade
            FROM acidentes.ocorrencias
            GROUP BY dia_semana
            ORDER BY total_acidentes DESC
        """)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"ClickHouse error: {e}")

    _cache[cache_key] = {"data": rows, "timestamp": time.time()}
    return rows
