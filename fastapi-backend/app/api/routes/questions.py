"""Questions API 路由"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
import app.crud.question as question_crud
import app.crud.question_material_link as link_crud
from app.services.pdf_export import build_questions_pdf

router = APIRouter(prefix="/questions", tags=["questions"])


class ExportPdfRequest(BaseModel):
    question_ids: list[int]


@router.put("/{question_id}/favourite")
def set_question_favourite(question_id: int, db: Session = Depends(get_db)):
    """设置题目收藏状态 favourite=1"""
    if not question_crud.update_favourite(db, question_id, 1):
        raise HTTPException(status_code=404, detail="Question not found")
    return {"ok": True}


@router.delete("/{question_id}/favourite")
def remove_question_favourite(question_id: int, db: Session = Depends(get_db)):
    """取消收藏 favourite=0"""
    if not question_crud.update_favourite(db, question_id, 0):
        raise HTTPException(status_code=404, detail="Question not found")
    return {"ok": True}


@router.get("/{question_id}/materials")
def get_question_materials(question_id: int, db: Session = Depends(get_db)):
    """获取题目关联的 Materials"""
    materials = link_crud.get_materials_by_question_id(db, question_id)
    return [
        {
            "material_id": m.material_id,
            "material_code": m.material_code,
            "material_type": m.material_type,
            "title": m.title,
            "file_path": m.file_path,
            "week_number": m.week_number,
        }
        for m in materials
    ]


@router.post("/export-pdf")
def export_questions_pdf(body: ExportPdfRequest, db: Session = Depends(get_db)):
    """将选定的题目合并导出为 PDF"""
    if not body.question_ids:
        raise HTTPException(status_code=400, detail="question_ids cannot be empty")
    questions_orm = question_crud.get_questions_by_ids(db, body.question_ids)
    if not questions_orm:
        raise HTTPException(status_code=404, detail="No questions found")
    questions_data = [
        {
            "question_code": q.question_code,
            "question_text": q.question_text,
            "answer_text": q.answer_text,
            "knowledge_point": q.knowledge_point,
            "source_type": q.source_type,
            "source_year": q.source_year,
        }
        for q in questions_orm
    ]
    pdf_bytes = build_questions_pdf(questions_data)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="questions.pdf"'},
    )


@router.get("")
def get_all_questions(favourite: int | None = None, db: Session = Depends(get_db)):
    """获取所有题目，可选 ?favourite=1 仅返回收藏题目"""
    result = question_crud.get_questions_all(db, favourite=favourite)
    return [
        {
            "question_id": q.question_id,
            "question_code": q.question_code,
            "course_name": q.course_name,
            "source_year": q.source_year,
            "source_type": q.source_type,
            "knowledge_point": q.knowledge_point,
            "question_text": q.question_text,
            "answer_text": q.answer_text,
            "image_path": q.image_path,
            "language": q.language or "C",
        }
        for q in result
    ]
