"""Materials 下载 API"""
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
import app.crud.material as material_crud

router = APIRouter(prefix="/materials", tags=["materials"])

def _get_static_root() -> Path:
    from app.config import settings

    if settings.STATIC_FILES_ROOT:
        p = Path(settings.STATIC_FILES_ROOT)
        if p.exists():
            return p
    roots = [
        Path(__file__).resolve().parent.parent.parent.parent.parent / "backend" / "static",
        Path.cwd() / "backend" / "static",
        Path.cwd().parent / "backend" / "static",
    ]
    for r in roots:
        if (r / "lectures").exists():
            return r
    return roots[0]


@router.get("/{material_id}/download")
def download_material(material_id: int, db: Session = Depends(get_db)):
    """根据 material_id 下载关联文件，强制 attachment"""
    material = material_crud.get_material_by_id_sync(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    STATIC_ROOT = _get_static_root()
    file_path = (material.file_path or "").strip()

    # file_path 可能是 /static/lectures/xxx.pdf 或 lectures/xxx.pdf 或纯文件名
    if file_path.startswith("/static/"):
        rel = file_path[len("/static/"):].lstrip("/")
    elif "/" in file_path:
        rel = file_path.lstrip("/")
    else:
        # 纯文件名：根据 material_type 推断目录
        type_dir = {"PPT": "lectures", "Lab": "labs", "CW": "courseworks", "Tutorial": "tutorials"}.get(
            str(material.material_type), "others"
        )
        rel = f"{type_dir}/{file_path}"

    full_path = (STATIC_ROOT / rel).resolve()
    base = str(STATIC_ROOT.resolve())
    if not str(full_path).startswith(base):
        raise HTTPException(status_code=403, detail="Invalid path")
    if not full_path.exists() or not full_path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {rel}",
        )

    filename = material.title or material.material_code or full_path.name
    if not filename.endswith(Path(file_path).suffix):
        filename = f"{filename}{Path(file_path).suffix}"

    return FileResponse(
        full_path,
        media_type="application/octet-stream",
        filename=filename,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
