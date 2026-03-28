"""Build AI session context from DB: full bank summary + current user's favourites."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

import app.crud.question as question_crud
from app.models.material import Material


def _truncate(text: str | None, max_len: int) -> str:
    if not text:
        return ""
    s = str(text).strip().replace("\r\n", "\n")
    if len(s) <= max_len:
        return s
    return s[: max_len - 1] + "…"


def build_ai_session_context(db: Session, user_id: int) -> dict:
    """
    Returns:
      context_text: plain text for LLM system message
      meta: counts for the frontend status line
    """
    materials_count = int(
        db.execute(select(func.count()).select_from(Material)).scalar() or 0
    )

    all_questions = question_crud.get_questions_all(db, skip=0, limit=10000)
    total_q = len(all_questions)

    favourites = question_crud.get_questions_all(db, user_id=user_id, favourite=1)
    fav_n = len(favourites)

    max_catalog = 600
    lines: list[str] = []
    lines.append("=== TERMINOLOGY — READ CAREFULLY (do not mix these up) ===")
    lines.append(
        f"- FULL CATALOG / \"all questions in the database\" / Questions table: {total_q} rows. "
        "This is the entire platform bank. It is NOT the user's Question Bank."
    )
    lines.append(
        f'- QUESTION BANK (UI) = ONLY this user\'s favourited questions (is_favourite=1): {fav_n} item(s). '
        "Always call this the Question Bank; never say the Question Bank has the full-catalog count."
    )
    lines.append(
        '- A single "question" = one row identified by question_id / question_code. '
        "Question Bank holds zero or more such questions that the user starred."
    )
    lines.append(f"- Materials table rows: {materials_count}")
    lines.append("")
    lines.append(
        f"SECTION A — FULL CATALOG SNIPPETS (first {min(max_catalog, total_q)} of {total_q} questions; NOT Question Bank)"
    )
    lines.append("")

    for q in all_questions[:max_catalog]:
        snippet = _truncate(q.question_text, 320)
        lines.append(
            f"- [question_id={q.question_id}] {q.question_code} | course={q.course_name} | "
            f"type={q.source_type} | year={q.source_year} | lang={q.language or 'C'} | kp={q.knowledge_point}\n"
            f"  stem excerpt: {snippet}"
        )
    if total_q > max_catalog:
        lines.append(f"... {total_q - max_catalog} more questions omitted from the list but counted in the total.")

    lines.append("")
    lines.append(
        f"SECTION B — QUESTION BANK ONLY (user_id={user_id}, is_favourite=1) — {fav_n} question(s), NOT {total_q}"
    )
    if fav_n == 0:
        lines.append("This user has no items in their Question Bank (no favourites).")
    else:
        lines.append("Full text (truncated) for each favourited question:")
        lines.append("")
        for q in favourites:
            lines.append(f"### {q.question_code} (question_id={q.question_id})")
            lines.append(
                f"Course: {q.course_name} | KP: {q.knowledge_point} | Lang: {q.language or 'C'} | Year: {q.source_year}"
            )
            lines.append("Stem:\n" + _truncate(q.question_text, 6000))
            if q.answer_text:
                lines.append("Reference answer:\n" + _truncate(q.answer_text, 6000))
            lines.append("")

    context_text = "\n".join(lines)
    return {
        "context_text": context_text,
        "meta": {
            "question_count": total_q,
            "favourite_count": fav_n,
            "materials_count": materials_count,
            "catalog_listed": min(max_catalog, total_q),
        },
    }
