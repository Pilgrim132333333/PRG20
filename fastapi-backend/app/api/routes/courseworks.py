"""Courseworks API 路由 - 数据来源于 Questions 表中 source_type='CW' 的题目"""
import re
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
import app.crud.question as question_crud

router = APIRouter(prefix="/courseworks", tags=["courseworks"])


@router.get("")
def get_all_courseworks(db: Session = Depends(get_db)):
    """获取所有作业（来自 Questions 表 source_type='CW'）"""
    rows = question_crud.select_all_coursework(db)
    def _course_code(name):
        if not name:
            return ""
        m = re.search(r"\d{4}", str(name))
        return m.group(0) if m else name

    return [
        {
            "question_id": q.question_id,
            "question_code": q.question_code,
            "title": q.question_code or ((q.question_text or "").split("\n")[0][:80] or "-"),
            "language": q.language or "C",
            "course_name": q.course_name or "",
            "course": _course_code(q.course_name) or q.course_name or "",
            "courseName": q.course_name or "",
            "knowledge_point": q.knowledge_point or "",
            "source_year": q.source_year,
            "deadline": None,
            "status": "pending",
            "score": None,
        }
        for q in rows
    ]
