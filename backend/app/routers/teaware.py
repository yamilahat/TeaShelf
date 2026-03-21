from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models.teaware import Teaware, TeawarePreferredType
from app.schemas.teaware import TeawareCreate, TeawareRead, TeawareUpdate

router = APIRouter(prefix="/teaware", tags=["teaware"])


@router.post("", response_model=TeawareRead, status_code=status.HTTP_201_CREATED)
def create_teaware(
    payload: TeawareCreate,
    db: Session = Depends(get_db_session),
) -> Teaware:
    teaware = Teaware(
        name=payload.name,
        nickname=payload.nickname,
        type=payload.type,
        volume_ml=payload.volume_ml,
        material=payload.material,
        vendor=payload.vendor,
        acquired_date=payload.acquired_date,
        notes=payload.notes,
        preferred_tea_types=[
            TeawarePreferredType(tea_type=t)
            for t in dict.fromkeys(t.value for t in payload.preferred_tea_types)
        ],
    )
    db.add(teaware)
    db.commit()
    db.refresh(teaware)
    return teaware


@router.get("", response_model=list[TeawareRead])
def list_teaware(db: Session = Depends(get_db_session)) -> list[Teaware]:
    return list(db.scalars(select(Teaware).order_by(Teaware.id.asc())).all())


@router.get("/{teaware_id}", response_model=TeawareRead)
def get_teaware(teaware_id: int, db: Session = Depends(get_db_session)) -> Teaware:
    teaware = db.get(Teaware, teaware_id)
    if not teaware:
        raise HTTPException(status_code=404, detail="Teaware not found")
    return teaware


@router.put("/{teaware_id}", response_model=TeawareRead)
def update_teaware(
    teaware_id: int,
    payload: TeawareUpdate,
    db: Session = Depends(get_db_session),
) -> Teaware:
    teaware = db.get(Teaware, teaware_id)
    if not teaware:
        raise HTTPException(status_code=404, detail="Teaware not found")

    update_data = payload.model_dump(exclude_unset=True)
    preferred_tea_types = update_data.pop("preferred_tea_types", None)

    for field, value in update_data.items():
        setattr(teaware, field, value)

    if preferred_tea_types is not None:
        teaware.preferred_tea_types = [
            TeawarePreferredType(tea_type=t)
            for t in dict.fromkeys(
                t.value if hasattr(t, "value") else t for t in preferred_tea_types
            )
        ]

    db.commit()
    db.refresh(teaware)
    return teaware


@router.delete("/{teaware_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teaware(teaware_id: int, db: Session = Depends(get_db_session)) -> Response:
    teaware = db.get(Teaware, teaware_id)
    if not teaware:
        raise HTTPException(status_code=404, detail="Teaware not found")

    db.delete(teaware)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
