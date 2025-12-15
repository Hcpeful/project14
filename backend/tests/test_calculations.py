import requests

BASE = "http://localhost:3001/calculations"

def test_add():
    r = requests.post(BASE, json={
        "operation": "add",
        "operandA": 2,
        "operandB": 3
    })
    assert r.status_code == 201
    assert r.json()["result"] == 5

def test_browse():
    r = requests.get(BASE)
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_read():
    r = requests.get(f"{BASE}/1")
    assert r.status_code == 200

def test_edit():
    r = requests.put(f"{BASE}/1", json={
        "operation": "multiply",
        "operandA": 2,
        "operandB": 4
    })
    assert r.json()["result"] == 8

def test_delete():
    r = requests.delete(f"{BASE}/1")
    assert r.status_code == 204
