"""Accela Records Service module"""
import sys
import json
import jsend
import falcon
from .hooks import validate_access
from .accela_svc import AccelaSvc

@falcon.before(validate_access)
class AccelaRecords(AccelaSvc):
    """ Records class """
    def on_get(self, _req, resp, **kwarg):
        """ GET requests for records """
        if 'ids' in kwarg:
            if not kwarg['ids']:
                resp.status = falcon.HTTP_400
                msg = "Record ids is required"
                resp.body = json.dumps(jsend.error(msg))
                return

            self.init()

            record_id = kwarg['ids']
            response = self.accela.records.get_records(record_id, None, 'AccessToken')

            # default
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(jsend.error(response.text))

            # if successful
            if response.status_code == 200:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(response.json())

        else:
            resp.status = falcon.HTTP_400
            msg = "Parameter missing"
            resp.body = json.dumps(jsend.error(msg))
            return

    def on_post(self, req, resp):
        """ POST requests for records """
        if 'fields' in req.params and req.content_length:
            params = req.params['fields']
            record = req.stream.read(sys.maxsize)

            self.init()
            response = self.accela.records.create_record(record, params)

            # default
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(jsend.error(response.text))

            # if successful
            if response.status_code == 200:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(response.json())
        else:
            resp.status = falcon.HTTP_400
            msg = "The create record information is missing"
            resp.body = json.dumps(jsend.error(msg))
            return
