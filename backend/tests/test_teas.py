from fastapi.testclient import TestClient


def test_create_tea_returns_created_tea(client: TestClient) -> None:
    payload = {
        "name": "Long Jing",
        "vendor": "Tea House",
        "origin": "China",
        "tea_type": "green",
        "harvest_year": 2024,
        "notes": "Chestnut aroma",
    }

    response = client.post("/teas", json=payload)

    assert response.status_code == 201
    assert response.json() == {"id": 1, **payload}


def test_list_teas_returns_teas_in_creation_order(client: TestClient) -> None:
    first = {"name": "Tie Guan Yin", "vendor": "Vendor A"}
    second = {"name": "Shou Mei", "vendor": "Vendor B"}

    client.post("/teas", json=first)
    client.post("/teas", json=second)

    response = client.get("/teas")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Tie Guan Yin",
            "vendor": "Vendor A",
            "origin": None,
            "tea_type": None,
            "harvest_year": None,
            "notes": None,
        },
        {
            "id": 2,
            "name": "Shou Mei",
            "vendor": "Vendor B",
            "origin": None,
            "tea_type": None,
            "harvest_year": None,
            "notes": None,
        },
    ]


def test_get_tea_returns_single_tea(client: TestClient) -> None:
    create_response = client.post("/teas", json={"name": "Gyokuro", "origin": "Japan"})
    tea_id = create_response.json()["id"]

    response = client.get(f"/teas/{tea_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": tea_id,
        "name": "Gyokuro",
        "vendor": None,
        "origin": "Japan",
        "tea_type": None,
        "harvest_year": None,
        "notes": None,
    }


def test_get_tea_returns_404_for_missing_tea(client: TestClient) -> None:
    response = client.get("/teas/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tea not found"}


def test_update_tea_replaces_existing_fields(client: TestClient) -> None:
    create_response = client.post("/teas", json={"name": "Old Name", "vendor": "Old Vendor"})
    tea_id = create_response.json()["id"]

    payload = {
        "name": "Da Hong Pao",
        "vendor": "Rock Tea Co",
        "origin": "China",
        "tea_type": "oolong",
        "harvest_year": 2023,
        "notes": "Roasted",
    }
    response = client.put(f"/teas/{tea_id}", json=payload)

    assert response.status_code == 200
    assert response.json() == {"id": tea_id, **payload}


def test_update_tea_returns_404_for_missing_tea(client: TestClient) -> None:
    response = client.put("/teas/999", json={"name": "Missing"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Tea not found"}


def test_delete_tea_removes_tea(client: TestClient) -> None:
    create_response = client.post("/teas", json={"name": "Bai Mudan"})
    tea_id = create_response.json()["id"]

    delete_response = client.delete(f"/teas/{tea_id}")
    get_response = client.get(f"/teas/{tea_id}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert get_response.status_code == 404


def test_delete_tea_returns_404_for_missing_tea(client: TestClient) -> None:
    response = client.delete("/teas/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tea not found"}
