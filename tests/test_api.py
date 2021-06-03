import pytest
from fastapi.testclient import TestClient
from chem_kit_api.main import app
from .data.transformations_from_smiles import (
    transformations_from_smiles,
)
from .data.smiles_from_smarts import smiles_from_smarts


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def test_transformations_from_smiles_422(client):
    response = client.post("/transformations_from_smiles")
    assert response.status_code == 422


@pytest.mark.parametrize("data", transformations_from_smiles)
def test_transformations_from_smiles_200(client, data):
    body_json = {"smiles": data["smiles"]}
    response = client.post("/transformations_from_smiles", json=body_json)
    assert response.status_code == 200
    assert response.json() == data["result"]


def test_smiles_from_smarts_422(client):
    response = client.post("/smiles_from_smarts")
    assert response.status_code == 422


@pytest.mark.parametrize("data", smiles_from_smarts)
def test_smiles_from_smarts_200(client, data):
    body_json = {"smarts": data["smarts"]}
    response = client.post("/smiles_from_smarts", json=body_json)
    assert response.status_code == 200
    assert response.json() == data["smiles"]