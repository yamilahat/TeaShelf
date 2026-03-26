from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db_session
from app.models.steep_infusion import SteepInfusion
from app.models.tea import Tea
from app.models.tea_session import TeaSession
from app.schemas.tea_session import SessionCreate, SessionRead, SessionUpdate

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: SessionCreate,
    db: Session = Depends(get_db_session),
) -> TeaSession:
    tea = db.get(Tea, payload.tea_id)
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")

    session_data = payload.model_dump(exclude={"steep_infusions"})
    tea_session = TeaSession(**session_data)
    db.add(tea_session)
    db.flush()
    for inf in payload.steep_infusions:
        db.add(SteepInfusion(session_id=tea_session.id, **inf.model_dump()))
    db.commit()
    db.refresh(tea_session)
    return tea_session


@router.get("", response_model=list[SessionRead])
def list_sessions(db: Session = Depends(get_db_session)) -> list[TeaSession]:
    stmt = (
        select(TeaSession)
        .options(selectinload(TeaSession.steep_infusions))
        .order_by(TeaSession.id.asc())
    )
    return list(db.scalars(stmt).all())


@router.get("/{session_id}", response_model=SessionRead)
def get_session(session_id: int, db: Session = Depends(get_db_session)) -> TeaSession:
    tea_session = db.get(
        TeaSession, session_id, options=[selectinload(TeaSession.steep_infusions)]
    )
    if not tea_session:
        raise HTTPException(status_code=404, detail="Tea session not found")
    return tea_session


@router.put("/{session_id}", response_model=SessionRead)
def update_session(
    session_id: int,
    payload: SessionUpdate,
    db: Session = Depends(get_db_session),
) -> TeaSession:
    tea_session = db.get(
        TeaSession, session_id, options=[selectinload(TeaSession.steep_infusions)]
    )
    if not tea_session:
        raise HTTPException(status_code=404, detail="Tea session not found")

    tea = db.get(Tea, payload.tea_id)
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")

    update_data = payload.model_dump(exclude_unset=True, exclude={"steep_infusions"})
    for field, value in update_data.items():
        setattr(tea_session, field, value)

    for old_inf in list(tea_session.steep_infusions):
        db.delete(old_inf)
    db.flush()

    for inf in payload.steep_infusions:
        tea_session.steep_infusions.append(SteepInfusion(**inf.model_dump()))

    db.commit()
    db.refresh(tea_session)
    return tea_session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, db: Session = Depends(get_db_session)) -> Response:
    tea_session = db.get(TeaSession, session_id)
    if not tea_session:
        raise HTTPException(status_code=404, detail="Tea session not found")

    db.delete(tea_session)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
