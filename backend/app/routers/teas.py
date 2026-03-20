from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
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
    tea_type: str | None = Query(default=None),
    vendor: str | None = Query(default=None),
    name: str | None = Query(default=None),
) -> list[Tea]:
    stmt = select(Tea).order_by(Tea.id.asc())
    if tea_type:
        stmt = stmt.where(Tea.tea_type == tea_type)
    if vendor:
        stmt = stmt.where(Tea.vendor == vendor)
    if name:
        stmt = stmt.where(Tea.name.ilike(f"%{name}%"))
    return list(db.scalars(stmt).all())


@router.get("/{tea_id}", response_model=TeaRead)
def get_tea(tea_id: int, db: Session = Depends(get_db_session)) -> Tea:
    tea = db.get(Tea, tea_id)
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    return tea


@router.put("/{tea_id}", response_model=TeaRead)
def update_tea(
    tea_id: int,
    payload: TeaUpdate,
    db: Session = Depends(get_db_session),
) -> Tea:
    tea = db.get(Tea, tea_id)
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tea, field, value)

    db.commit()
    db.refresh(tea)
    return tea


@router.delete("/{tea_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tea(tea_id: int, db: Session = Depends(get_db_session)) -> Response:
    tea = db.get(Tea, tea_id)
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")

    db.delete(tea)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
