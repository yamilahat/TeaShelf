from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models.tea_session import TeaSession
from app.schemas.tea_session import SessionCreate, SessionRead, SessionUpdate

router = APIRouter(prefix="/sessions", tags=["teas"])


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: SessionCreate,
    db: Session = Depends(get_db_session),
) -> TeaSession:
    tea_session = TeaSession(
        tea_id=payload.tea_id,
        session_date=payload.session_date,
        steeps_count=payload.steeps_count,
        rating=payload.rating,
        notes=payload.notes,
    )
    db.add(tea_session)
    db.commit()
    db.refresh(tea_session)
    return tea_session


# @router.get("", response_model=list[SessionRead])
# def list_teas(db: Session = Depends(get_db_session)) -> list[TeaSession]:
#     stmt = select(Tea).order_by(Tea.id.asc())
#     teas = list(db.scalars(stmt).all())
#     return teas


# @router.get("/{tea_id}", response_model=TeaRead)
# def get_tea(tea_id: int, db: Session = Depends(get_db_session)) -> Tea:
#     tea = db.get(Tea, tea_id)
#     if not tea:
#         raise HTTPException(status_code=404, detail="Tea not found")
#     return tea


# @router.put("/{tea_id}", response_model=TeaRead)
# def update_tea(
#     tea_id: int,
#     payload: TeaUpdate,
#     db: Session = Depends(get_db_session),
# ) -> Tea:
#     tea = db.get(Tea, tea_id)
#     if not tea:
#         raise HTTPException(status_code=404, detail="Tea not found")

#     update_data = payload.model_dump(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(tea, field, value)

#     db.commit()
#     db.refresh(tea)
#     return tea


# @router.delete("/{tea_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_tea(tea_id: int, db: Session = Depends(get_db_session)) -> Response:
#     tea = db.get(Tea, tea_id)
#     if not tea:
#         raise HTTPException(status_code=404, detail="Tea not found")

#     db.delete(tea)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
