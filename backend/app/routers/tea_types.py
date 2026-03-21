from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models.tea_type import TeaTypeRef
from app.schemas.tea_type import TeaTypeRead

router = APIRouter(prefix="/tea-types", tags=["tea-types"])


@router.get("", response_model=list[TeaTypeRead])
def list_tea_types(db: Session = Depends(get_db_session)) -> list[TeaTypeRef]:
    return list(db.scalars(select(TeaTypeRef).order_by(TeaTypeRef.id)).all())
