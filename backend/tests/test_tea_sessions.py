from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.steep_infusion import SteepInfusion
from app.models.tea_session import TeaSession


def create_tea(client: TestClient) -> int:
    response = client.post("/teas", json={"name": "Long Jing"})
    assert response.status_code == 201
    return response.json()["id"]


def session_payload(
    tea_id: int,
    session_date: str = "2024-05-01",
    steeps_count: int | None = 5,
    rating: int | None = 8,
    notes: str | None = "Sweet and grassy",
    teaware_id: int | None = None,
    water_temp_c: float | None = None,
    leaf_weight_g: float | None = None,
    water_volume_ml: float | None = None,
    brew_method: str | None = None,
    steep_infusions: list | None = None,
) -> dict:
    return {
        "tea_id": tea_id,
        "session_date": session_date,
        "steeps_count": steeps_count,
        "rating": rating,
        "notes": notes,
        "teaware_id": teaware_id,
        "water_temp_c": water_temp_c,
        "leaf_weight_g": leaf_weight_g,
        "water_volume_ml": water_volume_ml,
        "brew_method": brew_method,
        "steep_infusions": steep_infusions or [],
    }


def serialized_session_payload(payload: dict, session_id: int | None = None) -> dict:
    serialized = payload.copy()
    raw = serialized["session_date"]
    # Accept both YYYY-MM-DD (input) and DD/MM/YYYY (already serialized)
    try:
        d = date.fromisoformat(raw)
    except ValueError:
        d = date(int(raw[6:]), int(raw[3:5]), int(raw[:2]))
    serialized["session_date"] = d.strftime("%d/%m/%Y")
    serialized.setdefault("water_temp_c", None)
    serialized.setdefault("leaf_weight_g", None)
    serialized.setdefault("water_volume_ml", None)
    serialized.setdefault("brew_method", None)
    serialized.setdefault("steep_infusions", [])
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


def test_create_session_accepts_iso_date_format(client: TestClient) -> None:
    payload = session_payload(tea_id=create_tea(client), session_date="2024-05-01")

    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    assert response.json()["session_date"] == "01/05/2024"


def test_create_session_accepts_ddmmyyyy_format(client: TestClient) -> None:
    payload = session_payload(tea_id=create_tea(client), session_date="01/05/2024")

    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    assert response.json()["session_date"] == "01/05/2024"


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


def test_create_session_returns_422_for_invalid_date(client: TestClient) -> None:
    response = client.post(
        "/sessions",
        json={"tea_id": create_tea(client), "session_date": "not-a-date"},
    )

    assert response.status_code == 422


def test_create_session_returns_404_for_missing_tea(client: TestClient) -> None:
    response = client.post("/sessions", json=session_payload(tea_id=999))

    assert response.status_code == 404
    assert response.json() == {"detail": "Tea not found"}


def test_create_session_response_includes_session_id(client: TestClient) -> None:
    response = client.post("/sessions", json=session_payload(tea_id=create_tea(client)))

    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_list_sessions_returns_sessions_in_creation_order(client: TestClient) -> None:
    first_payload = session_payload(create_tea(client))
    second_payload = session_payload(
        tea_id=create_tea(client),
        session_date="2024-05-02",
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
        session_date="2024-06-10",
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

    response = client.put(f"/sessions/{session_id}", json=session_payload(tea_id=999))

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
        json={"tea_id": 1, "session_date": "2024-05-01"},
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


def test_create_session_with_teaware(client: TestClient) -> None:
    tea_id = create_tea(client)
    teaware_response = client.post("/teaware", json={"name": "Gaiwan"})
    teaware_id = teaware_response.json()["id"]

    payload = session_payload(tea_id=tea_id, teaware_id=teaware_id)
    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    assert response.json()["teaware_id"] == teaware_id


def test_create_session_teaware_id_is_optional(client: TestClient) -> None:
    payload = session_payload(tea_id=create_tea(client), teaware_id=None)

    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    assert response.json()["teaware_id"] is None


# --- Brew parameters ---


def test_create_session_with_all_brew_params(client: TestClient) -> None:
    payload = session_payload(
        tea_id=create_tea(client),
        water_temp_c=95.0,
        leaf_weight_g=5.5,
        water_volume_ml=100.0,
        brew_method="gongfu",
    )

    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["water_temp_c"] == 95.0
    assert body["leaf_weight_g"] == 5.5
    assert body["water_volume_ml"] == 100.0
    assert body["brew_method"] == "gongfu"


@pytest.mark.parametrize("field", ["water_temp_c", "leaf_weight_g", "water_volume_ml", "brew_method"])
def test_brew_param_is_null_when_omitted(client: TestClient, field: str) -> None:
    payload = session_payload(tea_id=create_tea(client))
    payload.pop(field)

    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    assert response.json()[field] is None


def test_brew_params_persisted_and_returned_on_get(
    client: TestClient,
) -> None:
    payload = session_payload(
        tea_id=create_tea(client),
        water_temp_c=80.0,
        leaf_weight_g=3.0,
        water_volume_ml=200.0,
        brew_method="western",
    )
    session_id = client.post("/sessions", json=payload).json()["id"]

    response = client.get(f"/sessions/{session_id}")

    body = response.json()
    assert body["water_temp_c"] == 80.0
    assert body["leaf_weight_g"] == 3.0
    assert body["water_volume_ml"] == 200.0
    assert body["brew_method"] == "western"


# --- Steep infusions ---


def test_create_session_with_steep_infusions_returns_them_with_ids(
    client: TestClient,
) -> None:
    payload = session_payload(
        tea_id=create_tea(client),
        steep_infusions=[
            {"steep_number": 1, "steep_time_seconds": 30},
            {"steep_number": 2, "steep_time_seconds": 45},
            {"steep_number": 3, "steep_time_seconds": 60},
        ],
    )

    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    infusions = response.json()["steep_infusions"]
    assert len(infusions) == 3
    by_steep = {i["steep_number"]: i for i in infusions}
    assert by_steep[1]["steep_time_seconds"] == 30
    assert by_steep[2]["steep_time_seconds"] == 45
    assert by_steep[3]["steep_time_seconds"] == 60
    assert all("id" in i and "session_id" in i for i in infusions)


def test_create_session_steep_infusions_default_to_empty_list(
    client: TestClient,
) -> None:
    payload = session_payload(tea_id=create_tea(client))
    payload.pop("steep_infusions")

    response = client.post("/sessions", json=payload)

    assert response.status_code == 201
    assert response.json()["steep_infusions"] == []


def test_get_session_returns_steep_infusions(
    client: TestClient,
) -> None:
    tea_id = create_tea(client)
    payload = session_payload(
        tea_id=tea_id,
        steep_infusions=[{"steep_number": 1, "steep_time_seconds": 20}],
    )
    session_id = client.post("/sessions", json=payload).json()["id"]

    response = client.get(f"/sessions/{session_id}")

    infusions = response.json()["steep_infusions"]
    assert len(infusions) == 1
    assert infusions[0]["steep_number"] == 1
    assert infusions[0]["steep_time_seconds"] == 20


def test_list_sessions_includes_steep_infusions(
    client: TestClient,
) -> None:
    payload = session_payload(
        tea_id=create_tea(client),
        steep_infusions=[{"steep_number": 1, "steep_time_seconds": 25}],
    )
    client.post("/sessions", json=payload)

    response = client.get("/sessions")

    assert response.status_code == 200
    infusions = response.json()[0]["steep_infusions"]
    assert len(infusions) == 1
    assert infusions[0]["steep_number"] == 1
    assert infusions[0]["steep_time_seconds"] == 25


def test_update_session_replaces_steep_infusions_entirely(
    client: TestClient,
) -> None:
    tea_id = create_tea(client)
    payload = session_payload(
        tea_id=tea_id,
        steep_infusions=[
            {"steep_number": 1, "steep_time_seconds": 30},
            {"steep_number": 2, "steep_time_seconds": 45},
        ],
    )
    session_id = client.post("/sessions", json=payload).json()["id"]

    updated = session_payload(
        tea_id=tea_id,
        steep_infusions=[{"steep_number": 1, "steep_time_seconds": 99}],
    )
    response = client.put(f"/sessions/{session_id}", json=updated)

    assert response.status_code == 200
    infusions = response.json()["steep_infusions"]
    assert len(infusions) == 1
    assert infusions[0]["steep_number"] == 1
    assert infusions[0]["steep_time_seconds"] == 99


def test_update_session_clears_steep_infusions_when_empty_list_sent(
    client: TestClient,
) -> None:
    tea_id = create_tea(client)
    payload = session_payload(
        tea_id=tea_id,
        steep_infusions=[{"steep_number": 1, "steep_time_seconds": 30}],
    )
    session_id = client.post("/sessions", json=payload).json()["id"]

    cleared = session_payload(tea_id=tea_id, steep_infusions=[])
    response = client.put(f"/sessions/{session_id}", json=cleared)

    assert response.status_code == 200
    assert response.json()["steep_infusions"] == []


def test_update_session_can_add_infusions_to_session_that_had_none(
    client: TestClient,
    db_session: Session,
) -> None:
    session_id, original = create_session(client, db_session)

    updated = session_payload(
        tea_id=original["tea_id"],
        steep_infusions=[
            {"steep_number": 1, "steep_time_seconds": 15},
            {"steep_number": 2, "steep_time_seconds": 20},
        ],
    )
    response = client.put(f"/sessions/{session_id}", json=updated)

    assert response.status_code == 200
    infusions = response.json()["steep_infusions"]
    assert len(infusions) == 2


def test_delete_session_removes_steep_infusions_from_database(
    client: TestClient,
    db_session: Session,
) -> None:
    tea_id = create_tea(client)
    payload = session_payload(
        tea_id=tea_id,
        steep_infusions=[
            {"steep_number": 1, "steep_time_seconds": 30},
            {"steep_number": 2, "steep_time_seconds": 45},
        ],
    )
    session_id = client.post("/sessions", json=payload).json()["id"]

    client.delete(f"/sessions/{session_id}")

    remaining = db_session.scalars(
        select(SteepInfusion).where(SteepInfusion.session_id == session_id)
    ).all()
    assert list(remaining) == []


# --- Steep infusion validation ---


def test_create_session_duplicate_steep_number_returns_422(
    client: TestClient,
) -> None:
    payload = session_payload(
        tea_id=create_tea(client),
        steep_infusions=[
            {"steep_number": 1, "steep_time_seconds": 30},
            {"steep_number": 1, "steep_time_seconds": 60},
        ],
    )

    response = client.post("/sessions", json=payload)

    assert response.status_code == 422


def test_update_session_duplicate_steep_number_returns_422(
    client: TestClient,
    db_session: Session,
) -> None:
    session_id, original = create_session(client, db_session)

    payload = session_payload(
        tea_id=original["tea_id"],
        steep_infusions=[
            {"steep_number": 2, "steep_time_seconds": 30},
            {"steep_number": 2, "steep_time_seconds": 60},
        ],
    )
    response = client.put(f"/sessions/{session_id}", json=payload)

    assert response.status_code == 422
