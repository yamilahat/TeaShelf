from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models.tea import Tea
from app.models.tea_type import TeaTypeRef as TeaType
from app.models.teaware import TeawarePreferredType
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


@router.put("/{tea_type_id}", response_model=TeaTypeRead)
def update_tea_type(
    tea_type_id: int,
    payload: TeaTypeUpdate,
    db: Session = Depends(get_db_session),
) -> TeaType:
    tea_type = db.get(TeaType, tea_type_id)
    if not tea_type:
        raise HTTPException(status_code=404, detail="Tea type not found")

    existing = db.scalars(
        select(TeaType).where(TeaType.name == payload.name, TeaType.id != tea_type_id)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Tea type {payload.name!r} already exists")

    tea_type.name = payload.name
    tea_type.category = payload.category
    db.commit()
    db.refresh(tea_type)
    return tea_type


@router.delete("/{tea_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tea_type(
    tea_type_id: int,
    db: Session = Depends(get_db_session),
) -> Response:
    tea_type = db.get(TeaType, tea_type_id)
    if not tea_type:
        raise HTTPException(status_code=404, detail="Tea type not found")

    tea_in_use = db.scalars(
        select(Tea.id).where(Tea.tea_type_id == tea_type_id).limit(1)
    ).first()
    if tea_in_use is not None:
        raise HTTPException(status_code=409, detail="Tea type is in use by teas")

    teaware_in_use = db.scalars(
        select(TeawarePreferredType.teaware_id)
        .where(TeawarePreferredType.tea_type_id == tea_type_id)
        .limit(1)
    ).first()
    if teaware_in_use is not None:
        raise HTTPException(
            status_code=409,
            detail="Tea type is in use by teaware preferred types",
        )

    db.delete(tea_type)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
