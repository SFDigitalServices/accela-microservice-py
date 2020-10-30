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

def test_create_record(client):
    """ Test Create Record """
    with open('tests/mocks/create_record_consolidated.json', 'r') as file_obj:
        mock_record = json.load(file_obj)

    assert mock_record

    if mock_record:

        mock_custom_forms = mock_record.pop('customForms', None)
        assert mock_custom_forms
        mock_custom_tables = mock_record.pop('customTables', None)
        assert mock_custom_tables

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

            # Test update_record_custom_forms
            response = client.simulate_put(
                '/records/'+record_id+'/customForms',
                body=json.dumps(mock_custom_forms))
            content = json.loads(response.content)
            assert response.status_code == 200
            if 'status' in content:
                assert content['status'] == 200

            # Test update_record_custom_tables
            response = client.simulate_put(
                '/records/'+record_id+'/customTables',
                body=json.dumps(mock_custom_tables))
            content = json.loads(response.content)

            assert response.status_code == 200
            if 'status' in content:
                assert content['status'] == 200

            # Test update_record_comments
            with open('tests/mocks/create_record_comments.json', 'r') as file_obj:
                mock_comments = json.load(file_obj)
            assert mock_comments

            response = client.simulate_put(
                '/records/'+record_id+'/comments',
                body=json.dumps(mock_comments))
            content = json.loads(response.content)

            assert response.status_code == 200
            if 'status' in content:
                assert content['status'] == 200

            # Test update_record_addresses
            with open('tests/mocks/create_record_addresses.json', 'r') as file_obj:
                mock_addresses = json.load(file_obj)
            assert mock_addresses

            response = client.simulate_put(
                '/records/'+record_id+'/addresses',
                body=json.dumps(mock_addresses))
            content = json.loads(response.content)

            assert response.status_code == 200
            if 'status' in content:
                assert content['status'] == 200
