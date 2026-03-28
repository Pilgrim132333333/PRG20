"""调用 OpenAI 兼容的 Chat Completions API（密钥与地址由配置提供）。"""
from __future__ import annotations

import httpx

from app.config import settings


def chat_completions(messages: list[dict]) -> str:
    """
    messages: OpenAI 格式 [{\"role\":\"system|user|assistant\",\"content\":\"...\"}, ...]
    返回助手文本内容。
    """
    key = (settings.AI_API_KEY or "").strip()
    if not key:
        raise ValueError("AI_API_KEY is not configured")

    base = (settings.AI_API_BASE or "https://api.openai.com/v1").rstrip("/")
    url = f"{base}/chat/completions"
    payload = {
        "model": settings.AI_MODEL,
        "messages": messages,
        "temperature": settings.AI_TEMPERATURE,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    timeout = httpx.Timeout(settings.AI_TIMEOUT_SECONDS, connect=30.0)
    with httpx.Client(timeout=timeout) as client:
        r = client.post(url, json=payload, headers=headers)
        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            detail = r.text[:2000] if r.text else str(e)
            raise RuntimeError(f"LLM HTTP {r.status_code}: {detail}") from e
        data = r.json()

    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError(f"LLM response missing choices: {data!r}"[:500])
    msg = choices[0].get("message") or {}
    content = msg.get("content")
    if content is None:
        raise RuntimeError(f"LLM response missing content: {data!r}"[:500])
    return str(content).strip()
