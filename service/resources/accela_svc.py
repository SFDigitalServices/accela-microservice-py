""" Base Accela Service module """
import os
from accela_rest_sdk.accela import Accela
class AccelaSvc:
    """ Base Accela Service class """

    accela = None

    def init(self):
        """ initialize accela """
        self.load_config()
        self.load_token()

    def load_config(self):
        """ load configuration """
        config = {}
        config['APP_ID'] = os.environ.get('ACCELA_APP_ID')
        config['APP_SECRET'] = os.environ.get('ACCELA_APP_SECRET')
        config['AGENCY'] = os.environ.get('ACCELA_AGENCY')

        self.accela = Accela(config)

    def load_token(self):
        """ load token """
        environment = os.environ.get('ACCELA_ENVIRONMENT')
        username = os.environ.get('ACCELA_USERNAME')
        password = os.environ.get('ACCELA_PASSWORD')
        scope = os.environ.get('ACCELA_SCOPE')

        self.accela.client.get_token(username, password, scope, environment)
    