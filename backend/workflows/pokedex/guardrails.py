"""
Guardrails Service
Detecção de jailbreak e validação de tópico para o Pokédex
"""

import json
import re
from dataclasses import dataclass
from typing import Tuple

from openai import AsyncOpenAI

from .config import (
    BLOCKED_KEYWORDS,
    BLOCKED_MESSAGE,
    JAILBREAK_THRESHOLD,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    TOPICAL_ALIGNMENT_PROMPT,
    TOPICAL_ALIGNMENT_THRESHOLD,
)


@dataclass
class GuardrailsResult:
    """Resultado da análise de guardrails"""
    passed: bool
    blocked_reason: str | None = None
    keyword_match: str | None = None
    topical_score: float | None = None


class GuardrailsService:
    """
    Serviço de guardrails para proteção contra:
    - Prompt injection
    - Jailbreak attempts
    - Off-topic content
    """

    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.blocked_keywords = [kw.lower() for kw in BLOCKED_KEYWORDS]

    def _check_keywords(self, text: str) -> Tuple[bool, str | None]:
        """
        Verifica se o texto contém keywords bloqueadas.

        Returns:
            Tuple[bool, str | None]: (is_blocked, matched_keyword)
        """
        text_lower = text.lower()

        for keyword in self.blocked_keywords:
            if keyword in text_lower:
                return True, keyword

        return False, None

    def _check_suspicious_patterns(self, text: str) -> bool:
        """
        Verifica padrões suspeitos que indicam tentativa de manipulação.
        """
        suspicious_patterns = [
            r"```.*system.*```",  # Tentativa de injetar system prompt
            r"\[INST\]",  # Marcadores de instrução
            r"\[/INST\]",
            r"<\|.*\|>",  # Tokens especiais
            r"###\s*(system|instruction|prompt)",  # Marcadores de seção
            r"(?:^|\s)IGNORE\s+(?:ALL\s+)?(?:PREVIOUS\s+)?(?:INSTRUCTIONS?)",
            r"(?:^|\s)FORGET\s+(?:ALL\s+)?(?:PREVIOUS\s+)?(?:INSTRUCTIONS?)",
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                return True

        return False

    async def _check_topical_alignment(self, text: str) -> Tuple[bool, float]:
        """
        Usa LLM para verificar se o texto está dentro do tópico permitido (Pokémon Gen 1).

        Returns:
            Tuple[bool, float]: (is_on_topic, confidence_score)
        """
        try:
            response = await self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": TOPICAL_ALIGNMENT_PROMPT},
                    {"role": "user", "content": f"Analise este texto: {text}"}
                ],
                temperature=0.1,
                max_completion_tokens=200
            )

            result_text = response.choices[0].message.content.strip()

            # Tenta extrair JSON da resposta
            try:
                # Remove possíveis backticks de markdown
                if "```" in result_text:
                    result_text = re.search(r"```(?:json)?\s*(.*?)\s*```", result_text, re.DOTALL)
                    if result_text:
                        result_text = result_text.group(1)

                result = json.loads(result_text)
                is_on_topic = result.get("is_on_topic", True)
                confidence = result.get("confidence", 0.5)

                return is_on_topic, confidence
            except json.JSONDecodeError:
                # Se não conseguir parsear, assume que está ok
                return True, 0.5

        except Exception as e:
            # Em caso de erro, permite a mensagem (fail open para não bloquear usuários)
            print(f"Error in topical alignment check: {e}")
            return True, 0.5

    async def check(self, text: str) -> GuardrailsResult:
        """
        Executa todas as verificações de guardrails.

        Args:
            text: Texto da pergunta do usuário

        Returns:
            GuardrailsResult: Resultado da análise
        """
        # 1. Verificar keywords bloqueadas
        is_blocked, matched_keyword = self._check_keywords(text)
        if is_blocked:
            return GuardrailsResult(
                passed=False,
                blocked_reason="Blocked keyword detected",
                keyword_match=matched_keyword
            )

        # 2. Verificar padrões suspeitos
        if self._check_suspicious_patterns(text):
            return GuardrailsResult(
                passed=False,
                blocked_reason="Suspicious pattern detected"
            )

        # 3. Verificar alinhamento de tópico (apenas para textos longos)
        if len(text) > 20:
            is_on_topic, confidence = await self._check_topical_alignment(text)

            if not is_on_topic and confidence >= TOPICAL_ALIGNMENT_THRESHOLD:
                return GuardrailsResult(
                    passed=False,
                    blocked_reason="Off-topic content",
                    topical_score=confidence
                )

        # Todas as verificações passaram
        return GuardrailsResult(passed=True)


# Instância singleton
_guardrails_service: GuardrailsService | None = None


def get_guardrails_service() -> GuardrailsService:
    """Retorna a instância singleton do serviço de guardrails."""
    global _guardrails_service
    if _guardrails_service is None:
        _guardrails_service = GuardrailsService()
    return _guardrails_service
