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


def test_create_tea_returns_422_for_unknown_tea_type(client: TestClient) -> None:
    response = client.post("/teas", json={"name": "Mystery Tea", "tea_type": "purple"})

    assert response.status_code == 422


def test_update_tea_returns_422_for_unknown_tea_type(client: TestClient) -> None:
    create_response = client.post("/teas", json={"name": "Long Jing"})
    tea_id = create_response.json()["id"]

    response = client.put(f"/teas/{tea_id}", json={"name": "Long Jing", "tea_type": "purple"})

    assert response.status_code == 422


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


# --- Milestone 5: filtering and search ---


def test_list_teas_filter_by_tea_type(client: TestClient) -> None:
    client.post("/teas", json={"name": "Long Jing", "tea_type": "green"})
    client.post("/teas", json={"name": "Da Hong Pao", "tea_type": "oolong"})

    response = client.get("/teas", params={"tea_type": "green"})

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Long Jing"


def test_list_teas_filter_by_vendor(client: TestClient) -> None:
    client.post("/teas", json={"name": "Gyokuro", "vendor": "Ippodo"})
    client.post("/teas", json={"name": "Sencha", "vendor": "Lupicia"})

    response = client.get("/teas", params={"vendor": "Ippodo"})

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Gyokuro"


def test_list_teas_filter_by_name_exact_match(client: TestClient) -> None:
    client.post("/teas", json={"name": "Gyokuro"})
    client.post("/teas", json={"name": "Bancha"})

    response = client.get("/teas", params={"name": "Gyokuro"})

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Gyokuro"


def test_list_teas_filter_by_name_partial_match(client: TestClient) -> None:
    client.post("/teas", json={"name": "Gyokuro"})
    client.post("/teas", json={"name": "Bancha"})

    response = client.get("/teas", params={"name": "yoku"})

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Gyokuro"


def test_list_teas_filter_by_name_case_insensitive(client: TestClient) -> None:
    client.post("/teas", json={"name": "Gyokuro"})

    response = client.get("/teas", params={"name": "GYOKURO"})

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Gyokuro"


def test_list_teas_filter_by_tea_type_no_match(client: TestClient) -> None:
    client.post("/teas", json={"name": "Long Jing", "tea_type": "green"})

    response = client.get("/teas", params={"tea_type": "white"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_teas_filter_by_vendor_no_match(client: TestClient) -> None:
    client.post("/teas", json={"name": "Gyokuro", "vendor": "Ippodo"})

    response = client.get("/teas", params={"vendor": "Unknown Vendor"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_teas_filter_by_name_no_match(client: TestClient) -> None:
    client.post("/teas", json={"name": "Gyokuro"})

    response = client.get("/teas", params={"name": "zzznomatch"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_teas_combined_tea_type_and_vendor(client: TestClient) -> None:
    client.post("/teas", json={"name": "Green A", "tea_type": "green", "vendor": "Ippodo"})
    client.post("/teas", json={"name": "Oolong A", "tea_type": "oolong", "vendor": "Ippodo"})
    client.post("/teas", json={"name": "Green B", "tea_type": "green", "vendor": "Lupicia"})

    response = client.get("/teas", params={"tea_type": "green", "vendor": "Ippodo"})

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Green A"


def test_list_teas_combined_name_and_tea_type(client: TestClient) -> None:
    client.post("/teas", json={"name": "Long Jing", "tea_type": "green"})
    client.post("/teas", json={"name": "Long An", "tea_type": "oolong"})

    response = client.get("/teas", params={"name": "Long", "tea_type": "green"})

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Long Jing"


def test_list_teas_combined_all_three_filters(client: TestClient) -> None:
    client.post("/teas", json={"name": "Gyokuro Special", "tea_type": "green", "vendor": "Ippodo"})
    client.post("/teas", json={"name": "Gyokuro Basic", "tea_type": "green", "vendor": "Lupicia"})
    client.post("/teas", json={"name": "Gyokuro Aged", "tea_type": "white", "vendor": "Ippodo"})

    response = client.get("/teas", params={"name": "Gyokuro", "tea_type": "green", "vendor": "Ippodo"})

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Gyokuro Special"


def test_list_teas_no_filters_returns_all(client: TestClient) -> None:
    client.post("/teas", json={"name": "Tea A", "tea_type": "green"})
    client.post("/teas", json={"name": "Tea B", "tea_type": "oolong"})
    client.post("/teas", json={"name": "Tea C"})

    response = client.get("/teas")

    assert response.status_code == 200
    assert len(response.json()) == 3
