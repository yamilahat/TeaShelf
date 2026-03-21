from fastapi.testclient import TestClient


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
