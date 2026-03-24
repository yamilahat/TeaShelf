from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db_session
from app.models.tea import Tea
from app.models.tea_type import TeaTypeRef
from app.schemas.tea import TeaCreate, TeaRead, TeaUpdate, TeaQuantityUpdate

router = APIRouter(prefix="/teas", tags=["teas"])


def _resolve_tea_type_id(db: Session, name: str) -> int:
    tea_type = db.scalars(
        select(TeaTypeRef).where(TeaTypeRef.name == name)
    ).first()
    if not tea_type:
        raise HTTPException(
            status_code=422, detail=f"Unknown tea type: {name!r}"
        )
    return tea_type.id


@router.post("", response_model=TeaRead, status_code=status.HTTP_201_CREATED)
def create_tea(
    payload: TeaCreate,
    db: Session = Depends(get_db_session),
) -> Tea:
    tea_type_id = None
    if payload.tea_type is not None:
        tea_type_id = _resolve_tea_type_id(db, payload.tea_type)

    tea = Tea(
        name=payload.name,
        vendor=payload.vendor,
        origin=payload.origin,
        tea_type_id=tea_type_id,
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
    in_stock: bool | None = Query(default=None),
) -> list[Tea]:
    stmt = (
        select(Tea)
        .options(selectinload(Tea.tea_type_ref))
        .order_by(Tea.id.asc())
    )
    if tea_type:
        stmt = stmt.join(Tea.tea_type_ref).where(
            TeaTypeRef.name.ilike(f"%{tea_type}%")
        )
    if vendor:
        stmt = stmt.where(Tea.vendor.ilike(f"%{vendor}%"))
    if name:
        stmt = stmt.where(Tea.name.ilike(f"%{name}%"))
    if in_stock is True:
        stmt = stmt.where(
            (Tea.current_quantity_g == None) | (Tea.current_quantity_g > 0)  # noqa: E711
        )
    elif in_stock is False:
        stmt = stmt.where(
            (Tea.current_quantity_g != None) & (Tea.current_quantity_g <= 0)  # noqa: E711
        )
    return list(db.scalars(stmt).all())


@router.get("/{tea_id}", response_model=TeaRead)
def get_tea(tea_id: int, db: Session = Depends(get_db_session)) -> Tea:
    tea = db.scalars(
        select(Tea)
        .options(selectinload(Tea.tea_type_ref))
        .where(Tea.id == tea_id)
    ).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    return tea


@router.put("/{tea_id}", response_model=TeaRead)
def update_tea(
    tea_id: int,
    payload: TeaUpdate,
    db: Session = Depends(get_db_session),
) -> Tea:
    tea = db.scalars(
        select(Tea)
        .options(selectinload(Tea.tea_type_ref))
        .where(Tea.id == tea_id)
    ).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")

    update_data = payload.model_dump(exclude_unset=True)

    tea_type_name = update_data.pop("tea_type", None)
    if tea_type_name is not None:
        tea.tea_type_id = _resolve_tea_type_id(db, tea_type_name)
    elif "tea_type" in payload.model_fields_set:
        tea.tea_type_id = None

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


@router.patch("/{tea_id}/quantity", response_model=TeaRead)
def update_quantity(tea_id: int, payload: TeaQuantityUpdate, db: Session = Depends(get_db_session)) -> Tea:
    tea = db.scalars(
        select(Tea)
        .options(selectinload(Tea.tea_type_ref))
        .where(Tea.id == tea_id)
    ).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    elif not payload.model_dump(exclude_unset=True):
        raise HTTPException(status_code=422, detail="No fields provided")
    
    tea.current_quantity_g = payload.current_quantity_g
    db.commit()
    db.refresh(tea)
    return tea
