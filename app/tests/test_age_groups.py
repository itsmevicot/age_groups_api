from fastapi import status
from fastapi.testclient import TestClient
import os

os.environ['ENVIRONMENT'] = 'test'

def test_create_age_group_success(client: TestClient):
    payload = {"name": "Test Group", "min_age": 10, "max_age": 20}
    response = client.post(
        "/age-groups/",
        json=payload,
        auth=("admin", "adminuser"),
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Group"
    assert data["min_age"] == 10
    assert data["max_age"] == 20
    assert "id" in data


def test_create_age_group_invalid_range(client: TestClient):
    payload = {"name": "Invalid", "min_age": 30, "max_age": 20}
    response = client.post(
        "/age-groups/",
        json=payload,
        auth=("admin", "adminuser"),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "min_age must be less than max_age" in response.json()["detail"]


def test_list_and_get_age_groups(client: TestClient):
    g1 = {"name": "G1", "min_age": 0, "max_age": 5}
    g2 = {"name": "G2", "min_age": 6, "max_age": 10}
    resp1 = client.post("/age-groups/", json=g1, auth=("admin", "adminuser"))
    resp2 = client.post("/age-groups/", json=g2, auth=("admin", "adminuser"))

    list_resp = client.get("/age-groups/", auth=("admin", "adminuser"))
    assert list_resp.status_code == status.HTTP_200_OK
    items = list_resp.json()
    assert len(items) == 2
    ids = {item["id"] for item in items}
    for item in items:
        get_resp = client.get(
            f"/age-groups/{item['id']}",
            auth=("admin", "adminuser"),
        )
        assert get_resp.status_code == status.HTTP_200_OK
        assert get_resp.json()["name"] in ["G1", "G2"]


def test_delete_age_group(client: TestClient):
    payload = {"name": "ToDelete", "min_age": 15, "max_age": 18}
    resp = client.post(
        "/age-groups/", json=payload, auth=("admin", "adminuser"),
    )
    group_id = resp.json()["id"]
    del_resp = client.delete(
        f"/age-groups/{group_id}", auth=("admin", "adminuser"),
    )
    assert del_resp.status_code == status.HTTP_204_NO_CONTENT
    get_resp = client.get(
        f"/age-groups/{group_id}", auth=("admin", "adminuser"),
    )
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND
