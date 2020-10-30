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
    CLIENT_HEADERS['X-ACCELA-USERNAME'] = os.environ.get('ACCELA_USERNAME')
    CLIENT_HEADERS['X-ACCELA-ENV'] = os.environ.get('ACCELA_ENVIRONMENT')
    return testing.TestClient(app=service.microservice.start_service(), headers=CLIENT_HEADERS)

def test_create_record(client):
    """ Test Create Record """
    with open('tests/mocks/create_record_consolidated.json', 'r') as file_obj:
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
            print(record_id)

            assert 'customId' in content['result']

            for custom_type in ['customForms', 'customTables', 'comments']:
                assert custom_type in content
                assert 'status' in content[custom_type]
                assert content[custom_type]['status'] == 200
