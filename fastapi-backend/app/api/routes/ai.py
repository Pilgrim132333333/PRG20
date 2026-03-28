"""AI assistant: session context (DB) and chat (external LLM)."""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.crud import user as user_crud
from app.database import get_db
from app.services.ai_context import build_ai_session_context
from app.services import ai_llm

router = APIRouter(prefix="/ai", tags=["ai"])


def _require_user(db: Session, user_id: int | None) -> int:
    if user_id is None:
        raise HTTPException(status_code=400, detail="user_id is required")
    u = user_crud.get_by_id(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return user_id


@router.get("/session-context")
def get_session_context(
    user_id: int | None = Query(None, description="Logged-in user Users.user_id"),
    db: Session = Depends(get_db),
):
    """
    Called when the assistant panel opens: reload Questions / Materials and the user's favourites.
    Same context text as POST /ai/chat uses internally.
    """
    uid = _require_user(db, user_id)
    built = build_ai_session_context(db, uid)
    return {
        "ok": True,
        "context_text": built["context_text"],
        "meta": built["meta"],
    }


class ChatMessageIn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=32000)


class ChatRequest(BaseModel):
    user_id: int
    messages: list[ChatMessageIn] = Field(..., min_length=1, max_length=50)


@router.post("/chat")
def post_chat(body: ChatRequest, db: Session = Depends(get_db)):
    """
    User/assistant turns; server rebuilds DB context and calls the LLM.
    Set AI_API_KEY (and optionally AI_API_BASE / AI_MODEL) in the environment.
    """
    _require_user(db, body.user_id)
    built = build_ai_session_context(db, body.user_id)
    context_text = built["context_text"]
    meta = built["meta"]
    n_all = meta.get("question_count", 0)
    n_bank = meta.get("favourite_count", 0)

    system_content = (
        'You are the study assistant for "AI Programming Question Bank". '
        "Help students understand questions, knowledge points, and programming ideas. "
        "Answer in clear, concise English unless the user writes in another language. "
        "When citing from the materials below, mention question_id or question_code.\n\n"
        "CRITICAL VOCABULARY:\n"
        f'- "Full catalog" / database Questions table = {n_all} questions total (entire platform).\n'
        f'- "Question Bank" (the user\'s saved/favourited list) = exactly {n_bank} question(s). '
        "It is ONLY Section B in the data below. Never equate Question Bank size with the full-catalog count.\n"
        "If the user asks about their Question Bank, use Section B and the number "
        f"{n_bank}. If they ask about the whole site bank, use {n_all}.\n\n"
        "----- Data from MySQL (Section A = full catalog; Section B = Question Bank) -----\n"
        + context_text
    )

    messages: list[dict] = [{"role": "system", "content": system_content}]
    for m in body.messages:
        messages.append({"role": m.role, "content": m.content})

    try:
        reply = ai_llm.chat_completions(messages)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e!s}") from e

    return {"ok": True, "reply": reply, "meta": built["meta"]}
