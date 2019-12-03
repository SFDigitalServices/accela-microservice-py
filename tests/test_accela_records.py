# pylint: disable=redefined-outer-name
"""Tests for accela_records.py"""
import os
import json
import pytest
from falcon import testing
import service.microservice

CLIENT_HEADERS = {
    "ACCESS_KEY": "1234567"
}

@pytest.fixture()
def client():
    """ client fixture """
    CLIENT_HEADERS['ACCESS_KEY'] = os.environ.get('ACCESS_KEY')
    return testing.TestClient(app=service.microservice.start_service(), headers=CLIENT_HEADERS)

def test_records_no_access_key():
    """ Test records endpoint with no access key """
    client_no_access_key = testing.TestClient(service.microservice.start_service())
    response = client_no_access_key.simulate_get('/records')
    assert response.status_code == 403

def test_get_records_ids(client):
    """ Test Get Records with ids """
    response = client.simulate_get('/records/CCSF-18CAP-00000-008YI')
    assert response.status_code == 200

    content = json.loads(response.content)

    assert content
    assert 'result' in content

    response = content['result'][0]

    possible_keys = ['name', 'status', 'id', 'description']
    assert len(list(set(response.keys() & possible_keys))) == len(possible_keys)

def test_get_records_empty(client):
    """ Test GET Records without parameters """
    response = client.simulate_get('/records')
    assert response.status_code == 400

    response = client.simulate_get('/records/')
    assert response.status_code == 400


def test_create_record(client):
    """ Test Create Record """
    with open('tests/mocks/create_record.json', 'r') as file_obj:
        mock_record = json.load(file_obj)

    assert mock_record

    if mock_record:
        response = client.simulate_post(
            '/records',
            params={'fields':'customId,id'}, body=json.dumps(mock_record))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'result' in content
        if 'result' in content:
            assert 'id' in content['result']
            assert 'customId' in content['result']

def test_create_record_empty(client):
    """ Test Create Record with empty post body """
    response = client.simulate_post('/records')
    assert response.status_code == 400
