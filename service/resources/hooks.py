""" hooks """
import os
import falcon

def validate_access(req, _resp, _resource, _params):
    """ validate access method """
    access_key = os.environ.get('ACCESS_KEY')
    if not access_key or req.get_header('ACCESS_KEY') != access_key:
        raise falcon.HTTPForbidden(description='Access Denied')

def validate_required_fields(req, _resp, _resource, _params, required_fields):
    """ validate required fields method """
    if 'headers' in required_fields:
        for field in required_fields['headers']:
            if not req.get_header(field):
                raise falcon.HTTPBadRequest(description='Missing '+field+' header')
