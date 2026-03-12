from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models.tea import Tea
from app.schemas.tea import TeaCreate, TeaRead, TeaUpdate

router = APIRouter(prefix="/teas", tags=["teas"])


@router.get("", response_model=list[TeaRead])
def list_teas(
    db: Session = Depends(get_db_session),
) -> list[Tea]:
    stmt = select(Tea).order_by(Tea.id.asc())
    teas = list(db.scalars(stmt).all())
    return teas
