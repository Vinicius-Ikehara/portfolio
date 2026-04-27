"""MCP server exposing Brazilian federal highway accident data.

Reuses the same ClickHouse-backed queries as the REST endpoints — this module
is a thin protocol adapter, not a parallel implementation. Mounted by
main.py at /mcp and protected by a bearer-token middleware.
"""
from typing import Any

from mcp.server.fastmcp import FastMCP

from .routers.acidentes_h3 import _query_clickhouse

mcp = FastMCP("acidentes-h3-brazil", streamable_http_path="/")

_BR_STATES = {
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO",
}

_ALLOWED_WEATHER = {
    "Chuva", "Céu Claro", "Garoa/Chuvisco", "Ignorado",
    "Nevoeiro/Neblina", "Nublado", "Sol", "Vento",
}

_DIMENSION_TO_SQL = {
    "hour": "substring(horario, 1, 2)",
    "day_of_week": "dia_semana",
    "cause": "causa_acidente",
    "highway": "concat('BR-', toString(br))",
    "state": "uf",
    "weather": "condicao_metereologica",
    "road_type": "tipo_pista",
    "accident_type": "tipo_acidente",
}


def _sanitize_state(state: str | None) -> str | None:
    if not state:
        return None
    s = str(state).strip().upper()
    return s if s in _BR_STATES else None


def _sanitize_highway(hw: Any) -> int | None:
    if hw is None:
        return None
    try:
        n = int(hw)
        return n if 1 <= n <= 999 else None
    except (TypeError, ValueError):
        return None


def _escape_sql_str(v: str, max_len: int = 100) -> str:
    """Escape single quotes and truncate — all user strings must pass through this."""
    return str(v).replace("'", "''")[:max_len]


def _valid_iso_date(d: Any) -> str | None:
    if not isinstance(d, str) or len(d) != 10 or d[4] != "-" or d[7] != "-":
        return None
    try:
        int(d[:4]); int(d[5:7]); int(d[8:10])
        return d
    except ValueError:
        return None


def _build_accident_filter(
    state: str | None = None,
    highway: Any = None,
    cause: str | None = None,
    accident_type: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    weather: str | None = None,
) -> str:
    """Build WHERE fragment from validated inputs. Returns '1' if no valid filter."""
    parts = []
    if s := _sanitize_state(state):
        parts.append(f"uf = '{s}'")
    if h := _sanitize_highway(highway):
        parts.append(f"br = {h}")
    if cause:
        parts.append(f"positionCaseInsensitive(causa_acidente, '{_escape_sql_str(cause)}') > 0")
    if accident_type:
        parts.append(f"positionCaseInsensitive(tipo_acidente, '{_escape_sql_str(accident_type)}') > 0")
    if d := _valid_iso_date(date_from):
        parts.append(f"data_inversa >= '{d}'")
    if d := _valid_iso_date(date_to):
        parts.append(f"data_inversa <= '{d}'")
    if weather and weather in _ALLOWED_WEATHER:
        parts.append(f"condicao_metereologica = '{_escape_sql_str(weather)}'")
    return " AND ".join(parts) if parts else "1"


@mcp.tool()
def get_overview() -> dict:
    """Overview of the Brazilian federal highway accident dataset.

    Returns totals and the period covered. Call this first to understand
    what data is available before running more specific queries.

    Source: Polícia Rodoviária Federal (PRF) — Brazilian Federal Highway Police.
    """
    rows = _query_clickhouse("""
        SELECT
            countDistinct(id) as total_accidents,
            sum(mortos) as total_deaths,
            sum(feridos_graves) as total_serious_injuries,
            sum(feridos_leves) as total_light_injuries,
            toString(min(data_inversa)) as period_start,
            toString(max(data_inversa)) as period_end,
            round(sum(mortos) * 100.0 / countDistinct(id), 2) as national_lethality_rate
        FROM acidentes.ocorrencias
    """)
    result = rows[0] if rows else {}
    result["data_source"] = "Polícia Rodoviária Federal (PRF) — Brazilian Federal Highway Police"
    result["coverage"] = "Federal highways (BR-xxx) across all 27 Brazilian states."
    return result


@mcp.tool()
def top_dangerous_hotspots(
    state: str | None = None,
    metric: str = "deaths",
    limit: int = 10,
) -> list[dict]:
    """Most dangerous H3 hexagonal cells on federal highways.

    Each result is a ~0.7 km² hex that covers one or more road segments,
    aggregated by accidents, deaths, or lethality rate.

    Args:
        state: Two-letter Brazilian state code ("SP", "RJ", "SC", ...). Optional.
        metric: "deaths" | "accidents" | "lethality" (default "deaths").
        limit: 1-50 (default 10).
    """
    limit = max(1, min(int(limit), 50))
    safe_state = _sanitize_state(state)

    where_parts = ["h3_index > toUInt64(0)"]
    if safe_state:
        where_parts.append(f"uf = '{safe_state}'")
    where = " AND ".join(where_parts)

    if metric == "accidents":
        order = "accidents DESC"
    elif metric == "lethality":
        order = "lethality_rate DESC, accidents DESC"
    else:
        order = "deaths DESC, accidents DESC"

    return _query_clickhouse(f"""
        SELECT
            h3ToString(h3_index) as h3_hex,
            h3ToGeo(h3_index).2 as center_lat,
            h3ToGeo(h3_index).1 as center_lng,
            countDistinct(id) as accidents,
            sum(mortos) as deaths,
            sum(feridos_graves) + sum(feridos_leves) as injuries,
            round(sum(mortos) * 100.0 / countDistinct(id), 2) as lethality_rate,
            any(municipio) as municipality,
            any(uf) as state,
            any(concat('BR-', toString(br))) as main_highway
        FROM acidentes.ocorrencias
        WHERE {where}
        GROUP BY h3_index
        HAVING accidents >= 2
        ORDER BY {order}
        LIMIT {limit}
    """)


@mcp.tool()
def query_accidents(
    state: str | None = None,
    highway: int | None = None,
    cause: str | None = None,
    accident_type: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    weather: str | None = None,
    min_deaths: int = 0,
    limit: int = 50,
) -> list[dict]:
    """Search individual accidents by flexible filters.

    All filters are optional; multiple combine with AND.
    Dates must be ISO format (YYYY-MM-DD).
    Valid weather values: Chuva, Céu Claro, Garoa/Chuvisco, Nevoeiro/Neblina,
    Nublado, Sol, Vento, Ignorado.

    Args:
        state: 2-letter state code.
        highway: BR highway number (e.g. 101 for BR-101).
        cause: substring match in causa_acidente (case-insensitive).
        accident_type: substring match in tipo_acidente (case-insensitive).
        date_from, date_to: ISO date range.
        weather: exact weather condition (see list above).
        min_deaths: minimum fatalities per accident.
        limit: 1-200 (default 50).
    """
    limit = max(1, min(int(limit), 200))
    where = _build_accident_filter(state, highway, cause, accident_type, date_from, date_to, weather)

    having = ""
    try:
        md = int(min_deaths)
        if md > 0:
            having = f"HAVING sum(mortos) >= {md}"
    except (TypeError, ValueError):
        pass

    return _query_clickhouse(f"""
        SELECT
            toString(id) as id,
            toString(data_inversa) as date,
            horario as time,
            dia_semana as day_of_week,
            fase_dia as day_phase,
            concat('BR-', toString(br)) as highway,
            km,
            municipio as municipality,
            uf as state,
            causa_acidente as cause,
            tipo_acidente as accident_type,
            classificacao_acidente as classification,
            condicao_metereologica as weather,
            tipo_pista as road_type,
            tracado_via as road_layout,
            latitude,
            longitude,
            sum(mortos) as deaths,
            sum(feridos_graves) as serious_injuries,
            sum(feridos_leves) as light_injuries,
            count() as people_involved
        FROM acidentes.ocorrencias
        WHERE {where}
        GROUP BY id, data_inversa, horario, dia_semana, fase_dia, br, km,
                 municipio, uf, causa_acidente, tipo_acidente,
                 classificacao_acidente, condicao_metereologica,
                 tipo_pista, tracado_via, latitude, longitude
        {having}
        ORDER BY deaths DESC, serious_injuries DESC, data_inversa DESC
        LIMIT {limit}
    """)


@mcp.tool()
def patterns_by_dimension(
    dimension: str,
    state: str | None = None,
    highway: int | None = None,
    cause: str | None = None,
) -> list[dict]:
    """Aggregate accident counts grouped by a dimension, with optional filters.

    Args:
        dimension: one of "hour", "day_of_week", "cause", "highway", "state",
                   "weather", "road_type", "accident_type".
        state, highway, cause: optional filters to narrow the aggregation.

    Returns list of {key, accidents, deaths, lethality_rate} ordered by accidents.
    """
    if dimension not in _DIMENSION_TO_SQL:
        return [{"error": f"Invalid dimension. Allowed: {sorted(_DIMENSION_TO_SQL.keys())}"}]
    group_expr = _DIMENSION_TO_SQL[dimension]
    where = _build_accident_filter(state=state, highway=highway, cause=cause)

    return _query_clickhouse(f"""
        SELECT
            {group_expr} as key,
            countDistinct(id) as accidents,
            sum(mortos) as deaths,
            round(sum(mortos) * 100.0 / countDistinct(id), 2) as lethality_rate
        FROM acidentes.ocorrencias
        WHERE {where}
        GROUP BY key
        ORDER BY accidents DESC
        LIMIT 50
    """)


@mcp.tool()
def accidents_near_location(
    lat: float,
    lng: float,
    radius_km: float = 5.0,
    limit: int = 30,
) -> list[dict]:
    """Find accidents within a radius of a geographic point.

    Useful for "accidents near <city>" — provide the city's lat/lng and a radius.

    Args:
        lat, lng: reference coordinates (decimal degrees).
        radius_km: search radius in km, 0.1 to 50 (default 5).
        limit: 1-100 (default 30). Ordered by severity then distance.
    """
    try:
        lat_f = float(lat)
        lng_f = float(lng)
    except (TypeError, ValueError):
        return [{"error": "Invalid coordinates"}]
    if not (-90 <= lat_f <= 90 and -180 <= lng_f <= 180):
        return [{"error": "Coordinates out of range"}]
    radius_km = max(0.1, min(float(radius_km), 50.0))
    radius_m = radius_km * 1000.0
    limit = max(1, min(int(limit), 100))

    return _query_clickhouse(f"""
        SELECT
            toString(id) as id,
            toString(data_inversa) as date,
            horario as time,
            concat('BR-', toString(br)) as highway,
            km,
            municipio as municipality,
            uf as state,
            causa_acidente as cause,
            tipo_acidente as accident_type,
            latitude,
            longitude,
            round(greatCircleDistance({lng_f}, {lat_f}, longitude, latitude)) as distance_meters,
            sum(mortos) as deaths,
            sum(feridos_graves) as serious_injuries,
            sum(feridos_leves) as light_injuries
        FROM acidentes.ocorrencias
        WHERE greatCircleDistance({lng_f}, {lat_f}, longitude, latitude) <= {radius_m}
          AND latitude != 0 AND longitude != 0
        GROUP BY id, data_inversa, horario, br, km, municipio, uf,
                 causa_acidente, tipo_acidente, latitude, longitude
        ORDER BY deaths DESC, serious_injuries DESC, distance_meters ASC
        LIMIT {limit}
    """)


@mcp.tool()
def get_hex_origins(h3_hex: str, limit: int = 50) -> list[dict]:
    """List individual accidents that compose a specific H3 hex cell.

    Typical flow: call top_dangerous_hotspots() first, then drill into a
    specific hex with this tool.

    Args:
        h3_hex: H3 index as hex string (e.g. "88dc59c561fffff").
        limit: 1-200 (default 50), ordered by severity.
    """
    if not (1 <= len(h3_hex) <= 20) or not all(c in "0123456789abcdefABCDEF" for c in h3_hex):
        return [{"error": "Invalid H3 hex index"}]
    try:
        h3_int = int(h3_hex, 16)
    except ValueError:
        return [{"error": "Invalid H3 hex index"}]
    limit = max(1, min(int(limit), 200))

    return _query_clickhouse(f"""
        SELECT
            toString(id) as id,
            toString(data_inversa) as date,
            horario as time,
            dia_semana as day_of_week,
            concat('BR-', toString(br)) as highway,
            km,
            municipio as municipality,
            uf as state,
            causa_acidente as cause,
            tipo_acidente as accident_type,
            classificacao_acidente as classification,
            condicao_metereologica as weather,
            latitude,
            longitude,
            sum(mortos) as deaths,
            sum(feridos_graves) as serious_injuries,
            sum(feridos_leves) as light_injuries
        FROM acidentes.ocorrencias
        WHERE h3_index = {h3_int}
        GROUP BY id, data_inversa, horario, dia_semana, br, km, municipio, uf,
                 causa_acidente, tipo_acidente, classificacao_acidente,
                 condicao_metereologica, latitude, longitude
        ORDER BY deaths DESC, serious_injuries DESC, data_inversa DESC
        LIMIT {limit}
    """)
