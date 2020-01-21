# pylint: disable=redefined-outer-name,duplicate-code
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
    response = client.simulate_get(
        '/records/CCSF-18CAP-00000-008YI',
        params={'expand':'customTables,customForms'})
    assert response.status_code == 200

    content = json.loads(response.content)

    assert content
    assert 'result' in content

    response = content['result'][0]

    possible_keys = ['name', 'status', 'id', 'description', 'customTables', 'customForms']
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
            record_id = content['result']['id']
            assert 'customId' in content['result']

            # Test update_record_custom_tables with invalid body
            response = client.simulate_put(
                '/records/'+record_id+'/customTables',
                params={'ids':record_id},
                body=json.dumps([{"id":"test"}]))
            assert response.status_code == 400

            # Test update_record_custom_tables
            with open('tests/mocks/update_record_custom_tables.json', 'r') as file_obj:
                mock_custom_tables = json.load(file_obj)

            assert mock_custom_tables
            response = client.simulate_put(
                '/records/'+record_id+'/customTables',
                params={'ids':record_id},
                body=json.dumps(mock_custom_tables))
            assert response.status_code == 200
            content = json.loads(response.content)
            if 'status' in content:
                assert content['status'] == 200

            # Test update_record_custom_forms
            with open('tests/mocks/update_record_custom_forms.json', 'r') as file_obj:
                mock_custom_forms = json.load(file_obj)

            assert mock_custom_tables
            response = client.simulate_put(
                '/records/'+record_id+'/customForms',
                params={'ids':record_id},
                body=json.dumps(mock_custom_forms))
            assert response.status_code == 200
            content = json.loads(response.content)
            if 'status' in content:
                assert content['status'] == 200

def test_create_record_empty(client):
    """ Test Create Record with empty post body """
    response = client.simulate_post('/records')
    assert response.status_code == 400

    response = client.simulate_post('/records', body='stuff')
    assert response.status_code == 400

def test_update_record_invalid(client):
    """ Test Update Record with invalid parameters """
    response = client.simulate_put('/records')
    assert response.status_code == 400

    response = client.simulate_put('/records/123')
    assert response.status_code == 400

    response = client.simulate_put('/records/123', body='stuff')
    assert response.status_code == 400

    response = client.simulate_put('/records/123/stuff', body='stuff')
    assert response.status_code == 400
