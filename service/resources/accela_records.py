"""Accela Records Service module"""
import sys
import json
import jsend
import falcon
import sentry_sdk
from .hooks import validate_access
from .accela_svc import AccelaSvc

@falcon.before(validate_access)
class AccelaRecords(AccelaSvc):
    """ Records class """
    def on_get(self, req, resp, **kwarg):
        """ GET requests for records """
        if 'ids' in kwarg:

            self.init()

            record_id = kwarg['ids']
            params = req.params
            response = self.accela.records.get_records(record_id, params, 'AccessToken')

            # default
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(jsend.error(response.text))

            # if successful
            if response.status_code == 200:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(response.json())
            else:
                with sentry_sdk.configure_scope() as scope:
                    scope.set_extra(
                        'get_records',
                        {'ids':record_id, 'params':params, 'response':response.text})
                sentry_sdk.capture_message('accela.get_records', 'error')

        else:
            resp.status = falcon.HTTP_400
            msg = "Record ids is required"
            resp.body = json.dumps(jsend.error(msg))
            return

    def on_post(self, req, resp):
        """ POST requests for records """

        if req.content_length:
            params = {}
            if req.params:
                params = req.params

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
                with sentry_sdk.configure_scope() as scope:
                    scope.set_extra(
                        'create_record',
                        {'params':params, 'record':record, 'response':response.text})
                sentry_sdk.capture_message('accela.create_record', 'error')
        else:
            resp.status = falcon.HTTP_400
            msg = "The create record information is missing"
            resp.body = json.dumps(jsend.error(msg))
            return

    def on_put(self, req, resp, **kwarg):
        """ PUT requests for records """
        if 'ids' in kwarg:

            self.init()

            record_ids = kwarg['ids']

            if req.content_length:

                params = {}
                if req.params:
                    params = req.params

                data = req.stream.read(sys.maxsize)

                if 'path' in kwarg:
                    path = kwarg['path']
                    response = None

                    if path == 'customForms':
                        response = self.accela.records.update_record_custom_forms(
                            record_ids, data, params)
                    elif path == 'customTables':
                        response = self.accela.records.update_record_custom_tables(
                            record_ids, data, params)

                    # if successful
                    if response is not None:
                        if response.status_code == 200:
                            resp.status = falcon.HTTP_200
                            resp.body = json.dumps(response.json())
                            return
                        resp.status = falcon.HTTP_400
                        resp.body = json.dumps(jsend.error(response.text))

                        with sentry_sdk.configure_scope() as scope:
                            scope.set_extra(path,
                                            {'ids':record_ids, 'params':params,
                                             'data':data, 'response':response.text})
                        sentry_sdk.capture_message('accela.'+path, 'error')
                        return

                    resp.status = falcon.HTTP_400
                    msg = "Path information is invalid"
                    resp.body = json.dumps(jsend.error(msg))
                    return

                resp.status = falcon.HTTP_400
                msg = "Path information is missing"
                resp.body = json.dumps(jsend.error(msg))
                return

            resp.status = falcon.HTTP_400
            msg = "Update information is missing"
            resp.body = json.dumps(jsend.error(msg))
            return

        resp.status = falcon.HTTP_400
        msg = "Record ids is required"
        resp.body = json.dumps(jsend.error(msg))
        return
