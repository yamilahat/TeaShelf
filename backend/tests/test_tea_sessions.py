from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tea_session import TeaSession


def create_tea(client: TestClient) -> int:
    response = client.post("/teas", json={"name": "Long Jing"})
    assert response.status_code == 201
    return response.json()["id"]


def session_payload(
    tea_id: int,
    session_date: str = "2024-05-01T09:30:00Z",
    steeps_count: int | None = 5,
    rating: int | None = 8,
    notes: str | None = "Sweet and grassy",
) -> dict:
    return {
        "tea_id": tea_id,
        "session_date": session_date,
        "steeps_count": steeps_count,
        "rating": rating,
        "notes": notes,
    }


def serialized_session_payload(payload: dict, session_id: int | None = None) -> dict:
    serialized = payload.copy()
    session_date = datetime.fromisoformat(
        serialized["session_date"].replace("Z", "+00:00")
    )
    serialized["session_date"] = (
        session_date.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    )
    if session_id is not None:
        serialized["id"] = session_id
    return serialized


def create_session(client: TestClient, db_session: Session) -> tuple[int, dict]:
    payload = session_payload(create_tea(client))

    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    session = db_session.scalar(select(TeaSession))
    assert session is not None
    return session.id, payload


def test_create_session_returns_created_session(client: TestClient) -> None:
    payload = session_payload(create_tea(client))

    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    assert response.json() == serialized_session_payload(payload, session_id=1)


def test_create_session_normalizes_offset_timestamps_to_utc(
    client: TestClient,
    db_session: Session,
) -> None:
    payload = session_payload(
        tea_id=create_tea(client),
        session_date="2024-05-01T12:30:00+03:00",
    )

    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    assert response.json() == {
        **serialized_session_payload(payload, session_id=1),
        "session_date": "2024-05-01T09:30:00Z",
    }

    session = db_session.scalar(select(TeaSession))
    assert session is not None
    assert session.session_date == datetime(
        2024,
        5,
        1,
        9,
        30,
        tzinfo=timezone.utc,
    )


def test_create_session_allows_optional_fields_to_be_null(client: TestClient) -> None:
    payload = session_payload(
        tea_id=create_tea(client),
        steeps_count=None,
        rating=None,
        notes=None,
    )

    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    assert response.json() == serialized_session_payload(payload, session_id=1)


def test_create_session_returns_422_when_required_fields_are_missing(
    client: TestClient,
) -> None:
    response = client.post("/sessions", json={"tea_id": 1})

    assert response.status_code == 422


def test_create_session_returns_422_for_naive_timestamps(client: TestClient) -> None:
    response = client.post(
        "/sessions",
        json={
            "tea_id": create_tea(client),
            "session_date": "2024-05-01T09:30:00",
        },
    )

    assert response.status_code == 422


def test_create_session_returns_404_for_missing_tea(client: TestClient) -> None:
    response = client.post(
        "/sessions",
        json=session_payload(tea_id=999),
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Tea not found"}


def test_create_session_response_includes_session_id(client: TestClient) -> None:
    response = client.post(
        "/sessions",
        json=session_payload(tea_id=create_tea(client)),
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_list_sessions_returns_sessions_in_creation_order(client: TestClient) -> None:
    first_payload = session_payload(create_tea(client))
    second_payload = session_payload(
        tea_id=create_tea(client),
        session_date="2024-05-02T11:00:00Z",
        steeps_count=7,
        rating=9,
        notes="Floral finish",
    )

    first_response = client.post("/sessions", json=first_payload)
    second_response = client.post("/sessions", json=second_payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    response = client.get("/sessions")

    assert response.status_code == 200
    assert response.json() == [
        serialized_session_payload(first_payload, session_id=1),
        serialized_session_payload(second_payload, session_id=2),
    ]


def test_list_sessions_includes_session_ids(
    client: TestClient,
    db_session: Session,
) -> None:
    session_id, payload = create_session(client, db_session)

    response = client.get("/sessions")

    assert response.status_code == 200
    assert response.json() == [serialized_session_payload(payload, session_id=session_id)]


def test_get_session_returns_single_session(
    client: TestClient,
    db_session: Session,
) -> None:
    session_id, payload = create_session(client, db_session)

    response = client.get(f"/sessions/{session_id}")

    assert response.status_code == 200
    assert response.json() == serialized_session_payload(payload, session_id=session_id)


def test_get_session_includes_session_id(
    client: TestClient,
    db_session: Session,
) -> None:
    session_id, payload = create_session(client, db_session)

    response = client.get(f"/sessions/{session_id}")

    assert response.status_code == 200
    assert response.json() == serialized_session_payload(payload, session_id=session_id)


def test_get_session_returns_404_for_missing_session(client: TestClient) -> None:
    response = client.get("/sessions/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tea session not found"}


def test_update_session_replaces_existing_fields(
    client: TestClient,
    db_session: Session,
) -> None:
    session_id, _ = create_session(client, db_session)
    payload = session_payload(
        tea_id=create_tea(client),
        session_date="2024-06-10T14:15:00Z",
        steeps_count=3,
        rating=6,
        notes="Shorter session",
    )

    response = client.put(f"/sessions/{session_id}", json=payload)

    assert response.status_code == 200
    assert response.json() == serialized_session_payload(payload, session_id=session_id)


def test_update_session_returns_404_for_missing_tea(
    client: TestClient,
    db_session: Session,
) -> None:
    session_id, _ = create_session(client, db_session)

    response = client.put(
        f"/sessions/{session_id}",
        json=session_payload(tea_id=999),
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Tea not found"}


def test_update_session_allows_clearing_optional_fields(
    client: TestClient,
    db_session: Session,
) -> None:
    session_id, original_payload = create_session(client, db_session)
    payload = session_payload(
        tea_id=original_payload["tea_id"],
        session_date=original_payload["session_date"],
        steeps_count=None,
        rating=None,
        notes=None,
    )

    response = client.put(f"/sessions/{session_id}", json=payload)

    assert response.status_code == 200
    assert response.json() == serialized_session_payload(payload, session_id=session_id)


def test_update_session_returns_404_for_missing_session(client: TestClient) -> None:
    response = client.put(
        "/sessions/999",
        json={
            "tea_id": 1,
            "session_date": "2024-05-01T09:30:00Z",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Tea session not found"}


def test_update_session_returns_422_when_required_fields_are_missing(
    client: TestClient,
    db_session: Session,
) -> None:
    session_id, _ = create_session(client, db_session)

    response = client.put(f"/sessions/{session_id}", json={"notes": "Incomplete"})

    assert response.status_code == 422


def test_delete_session_removes_session(
    client: TestClient,
    db_session: Session,
) -> None:
    session_id, _ = create_session(client, db_session)

    delete_response = client.delete(f"/sessions/{session_id}")
    get_response = client.get(f"/sessions/{session_id}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert get_response.status_code == 404


def test_delete_session_returns_404_for_missing_session(client: TestClient) -> None:
    response = client.delete("/sessions/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tea session not found"}


def test_session_routes_validate_integer_path_parameters(client: TestClient) -> None:
    response = client.get("/sessions/not-an-int")

    assert response.status_code == 422
