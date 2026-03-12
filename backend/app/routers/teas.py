from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models.tea import Tea
from app.schemas.tea import TeaCreate, TeaRead, TeaUpdate

router = APIRouter(prefix="/teas", tags=["teas"])


@router.post("", response_model=TeaRead, status_code=status.HTTP_201_CREATED)
def create_tea(
    payload: TeaCreate,
    db: Session = Depends(get_db_session),
) -> Tea:
    tea = Tea(
        name=payload.name,
        vendor=payload.vendor,
        origin=payload.origin,
        tea_type=payload.tea_type,
        harvest_year=payload.harvest_year,
        notes=payload.notes,
    )
    db.add(tea)
    db.commit()
    db.refresh(tea)
    return tea


@router.get("", response_model=list[TeaRead])
def list_teas(
    db: Session = Depends(get_db_session),
) -> list[Tea]:
    stmt = select(Tea).order_by(Tea.id.asc())
    teas = list(db.scalars(stmt).all())
    return teas
