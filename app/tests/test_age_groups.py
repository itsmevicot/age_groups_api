
def test_create_age_group_success(client):
    payload = {"name": "Test Group", "min_age": 10, "max_age": 20}
    response = client.post("/age-groups/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Group"
    assert data["min_age"] == 10
    assert data["max_age"] == 20
    assert "id" in data

def test_create_age_group_invalid_range(client):
    payload = {"name": "Invalid", "min_age": 30, "max_age": 20}
    response = client.post("/age-groups/", json=payload)
    assert response.status_code == 400
    assert "min_age must be less than max_age" in response.json()["detail"]

def test_list_and_get_age_groups(client):
    g1 = {"name": "G1", "min_age": 0, "max_age": 5}
    g2 = {"name": "G2", "min_age": 6, "max_age": 10}
    resp1 = client.post("/age-groups/", json=g1)
    resp2 = client.post("/age-groups/", json=g2)
    list_resp = client.get("/age-groups/")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert len(items) == 2
    ids = {item["id"] for item in items}
    for item in items:
        get_resp = client.get(f"/age-groups/{item['id']}")
        assert get_resp.status_code == 200
        assert get_resp.json()["name"] in ["G1", "G2"]

def test_delete_age_group(client):
    payload = {"name": "ToDelete", "min_age": 15, "max_age": 18}
    resp = client.post("/age-groups/", json=payload)
    group_id = resp.json()["id"]
    del_resp = client.delete(f"/age-groups/{group_id}")
    assert del_resp.status_code == 204
    get_resp = client.get(f"/age-groups/{group_id}")
    assert get_resp.status_code == 404
