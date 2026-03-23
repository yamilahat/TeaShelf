from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db_session

from app.models.tea_type import TeaTypeRef as TeaType
from app.schemas.tea_type import TeaTypeRead, TeaTypeCreate, TeaTypeUpdate

router = APIRouter(prefix="/tea-types", tags=["tea-types"])


@router.get("", response_model=list[TeaTypeRead])
def list_tea_types(db: Session = Depends(get_db_session)) -> list[TeaType]:
    return list(db.scalars(select(TeaType).order_by(TeaType.id)).all())


@router.post("", response_model=TeaTypeRead, status_code=status.HTTP_201_CREATED)
def create_tea_type(
    payload: TeaTypeCreate,
    db: Session = Depends(get_db_session),
) -> TeaType:
    existing = db.scalars(select(TeaType).where(TeaType.name == payload.name)).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Tea type {payload.name!r} already exists")

    tea_type = TeaType(name=payload.name, category=payload.category)
    db.add(tea_type)
    db.commit()
    db.refresh(tea_type)
    return tea_type
