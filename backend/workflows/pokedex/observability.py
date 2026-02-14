"""
Pokédex Observability Module
Configures Langfuse tracing via OpenTelemetry + OpenInference.

Uses OpenTelemetry with OTLP exporter to send traces to Langfuse's
OTLP endpoint. OpenInference instrumentors automatically capture:
- Agno agent runs, tool calls, and LLM interactions
- Direct OpenAI SDK calls (guardrails)
"""

import base64

from .config import (
    LANGFUSE_BASE_URL,
    LANGFUSE_ENABLED,
    LANGFUSE_PUBLIC_KEY,
    LANGFUSE_SECRET_KEY,
)

_initialized = False
_tracer_provider = None


def init_observability() -> None:
    """
    Initialize Langfuse observability via OpenTelemetry OTLP.

    Sets up a TracerProvider with OTLPSpanExporter pointing to Langfuse's
    OTLP ingestion endpoint, then instruments Agno and OpenAI SDK using
    OpenInference instrumentors.
    """
    global _initialized, _tracer_provider

    if _initialized:
        return

    if not LANGFUSE_ENABLED:
        print("[Observability] Langfuse disabled (LANGFUSE_ENABLED=false)")
        return

    if not LANGFUSE_SECRET_KEY or not LANGFUSE_PUBLIC_KEY:
        print("[Observability] Langfuse keys not configured, skipping")
        return

    try:
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )

        # Build Basic auth header: base64(public_key:secret_key)
        credentials = f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}"
        auth_token = base64.b64encode(credentials.encode()).decode()

        # Configure OTLP exporter pointing to Langfuse
        otlp_endpoint = f"{LANGFUSE_BASE_URL.rstrip('/')}/api/public/otel/v1/traces"
        exporter = OTLPSpanExporter(
            endpoint=otlp_endpoint,
            headers={"Authorization": f"Basic {auth_token}"},
            timeout=10,
        )

        # Set up TracerProvider with batch exporter (async, with retry)
        _tracer_provider = TracerProvider()
        _tracer_provider.add_span_processor(BatchSpanProcessor(exporter))

        # Register as global tracer provider
        from opentelemetry import trace
        trace.set_tracer_provider(_tracer_provider)

        # Instrument Agno (captures agent runs, tool calls, LLM calls)
        from openinference.instrumentation.agno import AgnoInstrumentor
        AgnoInstrumentor().instrument(tracer_provider=_tracer_provider)

        # Instrument OpenAI SDK (captures direct calls like guardrails)
        from openinference.instrumentation.openai import OpenAIInstrumentor
        OpenAIInstrumentor().instrument(tracer_provider=_tracer_provider)

        _initialized = True
        print(f"[Observability] Langfuse OTLP connected: {otlp_endpoint}")

    except Exception as e:
        print(f"[Observability] Init failed (non-blocking): {e}")
        _tracer_provider = None


def shutdown_observability() -> None:
    """Flush pending traces and shutdown gracefully."""
    global _initialized, _tracer_provider

    if not _initialized or _tracer_provider is None:
        return

    try:
        _tracer_provider.force_flush()
        _tracer_provider.shutdown()
        print("[Observability] Langfuse OTLP shutdown complete")
    except Exception as e:
        print(f"[Observability] Shutdown error: {e}")
    finally:
        _initialized = False
        _tracer_provider = None
