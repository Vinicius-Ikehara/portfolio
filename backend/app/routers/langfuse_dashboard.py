import time
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException

from ..config import settings

router = APIRouter(tags=["langfuse"])

# Simple in-memory cache with TTL
_cache: dict[str, Any] = {"data": None, "timestamp": 0}
_CACHE_TTL = 60  # seconds


def _is_cache_valid() -> bool:
    return _cache["data"] is not None and (time.time() - _cache["timestamp"]) < _CACHE_TTL


def _langfuse_auth() -> tuple[str, str]:
    return (settings.LANGFUSE_PUBLIC_KEY, settings.LANGFUSE_SECRET_KEY)


def _base_url() -> str:
    return settings.LANGFUSE_BASE_URL.rstrip("/")


async def _fetch_langfuse_data() -> dict:
    """Fetch traces and observations from Langfuse public API."""
    async with httpx.AsyncClient(timeout=15.0) as client:
        traces_resp = await client.get(
            f"{_base_url()}/api/public/traces",
            auth=_langfuse_auth(),
            params={"limit": 50, "orderBy": "timestamp.DESC"},
        )
        traces_resp.raise_for_status()
        traces_data = traces_resp.json()

        observations_resp = await client.get(
            f"{_base_url()}/api/public/observations",
            auth=_langfuse_auth(),
            params={"limit": 100, "orderBy": "startTime.DESC"},
        )
        observations_resp.raise_for_status()
        observations_data = observations_resp.json()

    return {
        "traces": traces_data.get("data", []),
        "observations": observations_data.get("data", []),
    }


def _build_summary(traces: list, observations: list) -> dict:
    """Compute summary metrics from raw data."""
    total_traces = len(traces)

    # Total cost from observations that have cost info
    total_cost = sum(
        obs.get("calculatedTotalCost") or 0
        for obs in observations
    )

    # Average latency from traces that have both start and end
    latencies = []
    for t in traces:
        start = t.get("timestamp")
        end = t.get("updatedAt") or t.get("timestamp")
        if start and end:
            from datetime import datetime, timezone
            try:
                t_start = datetime.fromisoformat(start.replace("Z", "+00:00"))
                t_end = datetime.fromisoformat(end.replace("Z", "+00:00"))
                latency_ms = (t_end - t_start).total_seconds() * 1000
                if latency_ms > 0:
                    latencies.append(latency_ms)
            except (ValueError, TypeError):
                pass

    avg_latency = round(sum(latencies) / len(latencies)) if latencies else 0

    return {
        "total_traces": total_traces,
        "total_cost_usd": round(total_cost, 4),
        "avg_latency_ms": avg_latency,
        "total_observations": len(observations),
    }


def _build_recent_traces(traces: list) -> list:
    """Format the 20 most recent traces for the frontend."""
    recent = []
    for t in traces[:20]:
        # Compute latency
        latency_ms = None
        start = t.get("timestamp")
        end = t.get("updatedAt") or t.get("timestamp")
        if start and end:
            from datetime import datetime
            try:
                t_start = datetime.fromisoformat(start.replace("Z", "+00:00"))
                t_end = datetime.fromisoformat(end.replace("Z", "+00:00"))
                latency_ms = round((t_end - t_start).total_seconds() * 1000)
            except (ValueError, TypeError):
                pass

        usage = t.get("usage") or {}
        recent.append({
            "id": t.get("id"),
            "name": t.get("name") or "unnamed",
            "timestamp": t.get("timestamp"),
            "latency_ms": latency_ms,
            "input_tokens": usage.get("input") or usage.get("promptTokens") or 0,
            "output_tokens": usage.get("output") or usage.get("completionTokens") or 0,
            "total_tokens": usage.get("total") or usage.get("totalTokens") or 0,
            "cost_usd": t.get("calculatedTotalCost") or 0,
            "status": "OK" if not t.get("level") or t.get("level") == "DEFAULT" else t.get("level"),
            "tags": t.get("tags", []),
        })
    return recent


def _build_daily_stats(traces: list) -> list:
    """Aggregate trace counts by day."""
    from collections import defaultdict
    daily: dict[str, int] = defaultdict(int)
    for t in traces:
        ts = t.get("timestamp", "")
        if ts:
            day = ts[:10]  # YYYY-MM-DD
            daily[day] += 1

    return [
        {"date": day, "traces": count}
        for day, count in sorted(daily.items(), reverse=True)
    ]


@router.get("/langfuse/dashboard")
async def get_langfuse_dashboard():
    """Return Langfuse dashboard metrics. Cached for 60s."""
    if not settings.LANGFUSE_ENABLED:
        return {"enabled": False}

    if not settings.LANGFUSE_PUBLIC_KEY or not settings.LANGFUSE_SECRET_KEY:
        return {"enabled": False}

    # Return cached data if valid
    if _is_cache_valid():
        return _cache["data"]

    try:
        raw = await _fetch_langfuse_data()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Langfuse API returned {e.response.status_code}",
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to connect to Langfuse: {e}",
        )

    traces = raw["traces"]
    observations = raw["observations"]

    result = {
        "enabled": True,
        "summary": _build_summary(traces, observations),
        "recent_traces": _build_recent_traces(traces),
        "daily_stats": _build_daily_stats(traces),
    }

    # Update cache
    _cache["data"] = result
    _cache["timestamp"] = time.time()

    return result
