from fastapi.testclient import TestClient


def teaware_payload(
    name: str = "Chaozhou Teapot",
    nickname: str | None = "the little one",
    teaware_type: str | None = "teapot",
    volume_ml: int | None = 80,
    material: str | None = "yixing clay",
    vendor: str | None = "Crimson Lotus",
    preferred_tea_types: list[str] = ["oolong"],
    acquired_date: str | None = "15/04/2023",
    notes: str | None = "Good for oolongs",
) -> dict:
    return {
        "name": name,
        "nickname": nickname,
        "type": teaware_type,
        "volume_ml": volume_ml,
        "material": material,
        "vendor": vendor,
        "preferred_tea_types": preferred_tea_types,
        "acquired_date": acquired_date,
        "notes": notes,
    }


def create_teaware(client: TestClient) -> tuple[int, dict]:
    payload = teaware_payload()
    response = client.post("/teaware", json=payload)
    assert response.status_code == 201
    return response.json()["id"], payload


# --- CREATE ---


def test_create_teaware_returns_created_teaware(client: TestClient) -> None:
    payload = teaware_payload()

    response = client.post("/teaware", json=payload)

    assert response.status_code == 201
    assert response.json() == {"id": 1, **payload}


def test_create_teaware_with_only_name(client: TestClient) -> None:
    payload = {"name": "Plain Mug"}

    response = client.post("/teaware", json=payload)

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Plain Mug",
        "nickname": None,
        "type": None,
        "volume_ml": None,
        "material": None,
        "vendor": None,
        "preferred_tea_types": [],
        "acquired_date": None,
        "notes": None,
    }


def test_create_teaware_returns_422_when_name_is_missing(client: TestClient) -> None:
    response = client.post("/teaware", json={"volume_ml": 100})

    assert response.status_code == 422


def test_create_teaware_with_multiple_preferred_types(client: TestClient) -> None:
    payload = teaware_payload(preferred_tea_types=["green", "white"])

    response = client.post("/teaware", json=payload)

    assert response.status_code == 201
    assert set(response.json()["preferred_tea_types"]) == {"green", "white"}


def test_create_teaware_returns_422_for_unknown_tea_type(client: TestClient) -> None:
    payload = teaware_payload(preferred_tea_types=["purple"])

    response = client.post("/teaware", json=payload)

    assert response.status_code == 422


def test_create_teaware_returns_422_for_mix_of_valid_and_invalid_types(
    client: TestClient,
) -> None:
    payload = teaware_payload(preferred_tea_types=["oolong", "purple"])

    response = client.post("/teaware", json=payload)

    assert response.status_code == 422


def test_create_teaware_with_empty_preferred_types(client: TestClient) -> None:
    payload = teaware_payload(preferred_tea_types=[])

    response = client.post("/teaware", json=payload)

    assert response.status_code == 201
    assert response.json()["preferred_tea_types"] == []


def test_create_teaware_response_includes_id(client: TestClient) -> None:
    response = client.post("/teaware", json=teaware_payload())

    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_create_teaware_acquired_date_returned_as_ddmmyyyy(client: TestClient) -> None:
    payload = teaware_payload(acquired_date="15/04/2023")

    response = client.post("/teaware", json=payload)

    assert response.status_code == 201
    assert response.json()["acquired_date"] == "15/04/2023"


def test_create_teaware_acquired_date_accepts_iso_input(client: TestClient) -> None:
    payload = teaware_payload(acquired_date="2023-04-15")

    response = client.post("/teaware", json=payload)

    assert response.status_code == 201
    assert response.json()["acquired_date"] == "15/04/2023"


def test_create_teaware_returns_422_for_invalid_date_format(client: TestClient) -> None:
    payload = teaware_payload(acquired_date="not-a-date")

    response = client.post("/teaware", json=payload)

    assert response.status_code == 422


# --- LIST ---


def test_list_teaware_returns_empty_list(client: TestClient) -> None:
    response = client.get("/teaware")

    assert response.status_code == 200
    assert response.json() == []


def test_list_teaware_returns_items_in_creation_order(client: TestClient) -> None:
    first_payload = teaware_payload(name="Gaiwan")
    second_payload = teaware_payload(name="Kyusu")

    first_response = client.post("/teaware", json=first_payload)
    second_response = client.post("/teaware", json=second_payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    response = client.get("/teaware")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Gaiwan"
    assert data[1]["name"] == "Kyusu"


def test_list_teaware_includes_ids(client: TestClient) -> None:
    client.post("/teaware", json=teaware_payload(name="Gaiwan"))
    client.post("/teaware", json=teaware_payload(name="Kyusu"))

    response = client.get("/teaware")

    assert response.status_code == 200
    data = response.json()
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2


# --- GET ---


def test_get_teaware_returns_single_item(client: TestClient) -> None:
    teaware_id, payload = create_teaware(client)

    response = client.get(f"/teaware/{teaware_id}")

    assert response.status_code == 200
    assert response.json() == {"id": teaware_id, **payload}


def test_get_teaware_returns_404_for_missing_item(client: TestClient) -> None:
    response = client.get("/teaware/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Teaware not found"}


def test_teaware_routes_validate_integer_path_parameters(client: TestClient) -> None:
    response = client.get("/teaware/not-an-int")

    assert response.status_code == 422


# --- UPDATE ---


def test_update_teaware_replaces_existing_fields(client: TestClient) -> None:
    teaware_id, _ = create_teaware(client)
    updated_payload = teaware_payload(
        name="Updated Gaiwan",
        nickname="new nickname",
        teaware_type="gaiwan",
        volume_ml=120,
        material="porcelain",
        vendor="White2Tea",
        preferred_tea_types=["green", "white"],
        notes="Updated notes",
    )

    response = client.put(f"/teaware/{teaware_id}", json=updated_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == teaware_id
    assert data["name"] == "Updated Gaiwan"
    assert set(data["preferred_tea_types"]) == {"green", "white"}


def test_update_teaware_returns_404_for_missing_item(client: TestClient) -> None:
    response = client.put("/teaware/999", json=teaware_payload())

    assert response.status_code == 404
    assert response.json() == {"detail": "Teaware not found"}


def test_update_teaware_allows_clearing_optional_fields(client: TestClient) -> None:
    teaware_id, _ = create_teaware(client)
    cleared_payload = teaware_payload(
        nickname=None,
        teaware_type=None,
        volume_ml=None,
        material=None,
        vendor=None,
        preferred_tea_types=[],
        acquired_date=None,
        notes=None,
    )

    response = client.put(f"/teaware/{teaware_id}", json=cleared_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nickname"] is None
    assert data["type"] is None
    assert data["volume_ml"] is None
    assert data["material"] is None
    assert data["vendor"] is None
    assert data["preferred_tea_types"] == []
    assert data["acquired_date"] is None
    assert data["notes"] is None


def test_update_teaware_returns_422_when_name_is_missing(client: TestClient) -> None:
    teaware_id, _ = create_teaware(client)

    response = client.put(f"/teaware/{teaware_id}", json={"notes": "Incomplete"})

    assert response.status_code == 422


def test_update_teaware_returns_422_for_unknown_tea_type(client: TestClient) -> None:
    teaware_id, _ = create_teaware(client)

    response = client.put(
        f"/teaware/{teaware_id}",
        json=teaware_payload(preferred_tea_types=["purple"]),
    )

    assert response.status_code == 422


def test_update_teaware_allows_changing_preferred_types(client: TestClient) -> None:
    teaware_id, _ = create_teaware(client)

    response = client.put(
        f"/teaware/{teaware_id}",
        json=teaware_payload(preferred_tea_types=["shou pu-erh (ripe)", "sheng pu-erh (raw)"]),
    )

    assert response.status_code == 200
    assert set(response.json()["preferred_tea_types"]) == {"shou pu-erh (ripe)", "sheng pu-erh (raw)"}


# --- DELETE ---


def test_delete_teaware_removes_item(client: TestClient) -> None:
    teaware_id, _ = create_teaware(client)

    delete_response = client.delete(f"/teaware/{teaware_id}")
    get_response = client.get(f"/teaware/{teaware_id}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert get_response.status_code == 404


def test_delete_teaware_returns_404_for_missing_item(client: TestClient) -> None:
    response = client.delete("/teaware/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Teaware not found"}


# --- Edge cases ---


def test_all_valid_tea_types_are_accepted(client: TestClient) -> None:
    all_types = ["green", "white", "black", "red", "yellow", "oolong", "shou pu-erh (ripe)", "sheng pu-erh (raw)"]
    payload = teaware_payload(preferred_tea_types=all_types)

    response = client.post("/teaware", json=payload)

    assert response.status_code == 201
    assert set(response.json()["preferred_tea_types"]) == set(all_types)


def test_duplicate_preferred_types_are_deduplicated(client: TestClient) -> None:
    payload = teaware_payload(preferred_tea_types=["oolong", "oolong"])

    response = client.post("/teaware", json=payload)

    assert response.status_code == 201
    assert response.json()["preferred_tea_types"].count("oolong") == 1
