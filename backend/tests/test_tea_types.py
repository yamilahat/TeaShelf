from fastapi.testclient import TestClient


# --- LIST ---


def test_list_tea_types_returns_all_seeded_types(client: TestClient) -> None:
    response = client.get("/tea-types")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 8
    names = {t["name"] for t in data}
    assert "green" in names
    assert "shou pu-erh (ripe)" in names


def test_list_tea_types_includes_category(client: TestClient) -> None:
    response = client.get("/tea-types")

    data = response.json()
    puerh_types = [t for t in data if t["category"] == "pu-erh"]
    assert len(puerh_types) == 2


def test_list_tea_types_returns_id_name_category(client: TestClient) -> None:
    response = client.get("/tea-types")

    data = response.json()
    first = data[0]
    assert "id" in first
    assert "name" in first
    assert "category" in first


# --- CREATE ---


def test_create_tea_type_returns_created_type(client: TestClient) -> None:
    response = client.post("/tea-types", json={"name": "herbal", "category": "herbal"})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "herbal"
    assert data["category"] == "herbal"
    assert "id" in data


def test_create_tea_type_returns_409_for_duplicate_name(client: TestClient) -> None:
    response = client.post("/tea-types", json={"name": "green", "category": "green"})

    assert response.status_code == 409


def test_create_tea_type_returns_422_when_name_is_missing(client: TestClient) -> None:
    response = client.post("/tea-types", json={"category": "herbal"})

    assert response.status_code == 422


def test_create_tea_type_returns_422_when_category_is_missing(client: TestClient) -> None:
    response = client.post("/tea-types", json={"name": "herbal"})

    assert response.status_code == 422


# --- UPDATE ---


def test_update_tea_type_returns_updated_type(client: TestClient) -> None:
    create_response = client.post("/tea-types", json={"name": "herbal", "category": "herbal"})
    tea_type_id = create_response.json()["id"]

    response = client.put(f"/tea-types/{tea_type_id}", json={"name": "herbal blend", "category": "herbal"})

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tea_type_id
    assert data["name"] == "herbal blend"
    assert data["category"] == "herbal"


def test_update_tea_type_returns_404_for_missing_type(client: TestClient) -> None:
    response = client.put("/tea-types/999", json={"name": "herbal", "category": "herbal"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Tea type not found"}


def test_update_tea_type_returns_409_for_duplicate_name(client: TestClient) -> None:
    response = client.put("/tea-types/1", json={"name": "black", "category": "green"})

    assert response.status_code == 409


def test_update_tea_type_allows_same_name(client: TestClient) -> None:
    response = client.put("/tea-types/1", json={"name": "green", "category": "green"})

    assert response.status_code == 200


# --- DELETE ---


def test_delete_tea_type_removes_type(client: TestClient) -> None:
    create_response = client.post("/tea-types", json={"name": "herbal", "category": "herbal"})
    tea_type_id = create_response.json()["id"]

    delete_response = client.delete(f"/tea-types/{tea_type_id}")
    list_response = client.get("/tea-types")

    assert delete_response.status_code == 204
    assert delete_response.content == b""
    names = {t["name"] for t in list_response.json()}
    assert "herbal" not in names


def test_delete_tea_type_returns_404_for_missing_type(client: TestClient) -> None:
    response = client.delete("/tea-types/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tea type not found"}


def test_delete_tea_type_returns_409_when_referenced_by_tea(client: TestClient) -> None:
    client.post("/teas", json={"name": "Long Jing", "tea_type": "green"})

    response = client.delete("/tea-types/1")  # id=1 is "green"

    assert response.status_code == 409


def test_delete_tea_type_returns_409_when_referenced_by_teaware(client: TestClient) -> None:
    client.post("/teaware", json={"name": "Gaiwan", "preferred_tea_types": ["oolong"]})

    oolong_id = next(
        t["id"] for t in client.get("/tea-types").json() if t["name"] == "oolong"
    )
    response = client.delete(f"/tea-types/{oolong_id}")

    assert response.status_code == 409


def test_delete_tea_type_succeeds_when_not_referenced(client: TestClient) -> None:
    create_response = client.post("/tea-types", json={"name": "herbal", "category": "herbal"})
    tea_type_id = create_response.json()["id"]

    response = client.delete(f"/tea-types/{tea_type_id}")

    assert response.status_code == 204
