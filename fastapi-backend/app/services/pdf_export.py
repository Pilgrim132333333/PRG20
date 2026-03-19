"""将选定题目合并导出为 PDF"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def _register_fonts():
    """尝试注册支持中文的字体（若系统存在），.ttf 格式"""
    for path, name in [
        ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "ArialUnicode"),
        ("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", "WenQuanYi"),
        ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", "NotoSansCJK"),
        ("C:/Windows/Fonts/msyh.ttf", "SimHei"),
    ]:
        try:
            pdfmetrics.registerFont(TTFont(name, path))
            return name
        except Exception:
            continue
    return None


def build_questions_pdf(questions: list) -> bytes:
    """
    将题目列表合并为一个 PDF。
    questions: [{"question_code", "question_text", "answer_text", "knowledge_point", ...}, ...]
    """
    buf = io.BytesIO()
    cjk_font = _register_fonts()
    style_title = ParagraphStyle(
        "Title",
        fontName=cjk_font or "Helvetica-Bold",
        fontSize=14,
        spaceAfter=6,
    )
    style_body = ParagraphStyle(
        "Body",
        fontName=cjk_font or "Helvetica",
        fontSize=10,
        spaceAfter=4,
    )
    style_code = ParagraphStyle(
        "Code",
        fontName="Courier",
        fontSize=9,
        spaceAfter=8,
        leftIndent=20,
        rightIndent=20,
        backColor="#f5f5f5",
    )

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    story = []

    for i, q in enumerate(questions, 1):
        code = (q.get("question_code") or "Question").replace("<", "&lt;").replace(">", "&gt;")
        title = f"<b>{i}. {code}</b>"
        story.append(Paragraph(title, style_title))

        meta_parts = []
        if q.get("knowledge_point"):
            meta_parts.append(f"Knowledge: {q['knowledge_point']}")
        if q.get("source_type"):
            meta_parts.append(f"Type: {q['source_type']}")
        if meta_parts:
            story.append(Paragraph(" | ".join(meta_parts), style_body))

        qtext = (q.get("question_text") or "").strip()
        if qtext:
            qtext_esc = qtext.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
            story.append(Paragraph("<b>Question:</b>", style_body))
            story.append(Paragraph(qtext_esc, style_body))
            story.append(Spacer(1, 4))

        ans = (q.get("answer_text") or "").strip()
        if ans:
            story.append(Paragraph("<b>Answer:</b>", style_body))
            story.append(Preformatted(ans, style_code))

        story.append(Spacer(1, 12))

    if not story:
        story.append(Paragraph("No questions selected.", style_body))

    doc.build(story)
    return buf.getvalue()
