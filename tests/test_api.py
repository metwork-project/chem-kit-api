import pytest
from fastapi.testclient import TestClient
from chem_kit_api.main import app
from .data import transformations_from_smiles_examples


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def test_transformations_from_smiles_422(client):
    response = client.post("/transformations_from_smiles")
    assert response.status_code == 422


@pytest.mark.parametrize("data", transformations_from_smiles_examples)
def test_transformations_from_smiles_200(client, data):
    body_json = {"smiles": data["smiles"]}
    response = client.post("/transformations_from_smiles", json=body_json)
    assert response.status_code == 200
    print(response.json())
    assert response.json() == data["result"]
