""" Base Accela Service module """
import os
from accela_rest_sdk.accela import Accela
class AccelaSvc:
    """ Base Accela Service class """

    accela = None

    def init(self, opt):
        """ initialize accela """
        if('ACCELA_ENVIRONMENT' in opt and 'ACCELA_USERNAME' in opt):
            env = opt['ACCELA_ENVIRONMENT']
            user = opt['ACCELA_USERNAME']
            self.load_config()
            self.load_token(env, user)

    def load_config(self):
        """ load configuration """
        config = {}
        config['APP_ID'] = os.environ.get('ACCELA_APP_ID')
        config['APP_SECRET'] = os.environ.get('ACCELA_APP_SECRET')
        config['AGENCY'] = os.environ.get('ACCELA_AGENCY')

        self.accela = Accela(config)

    def load_token(self, environment, username):
        """ load token """
        password = os.environ.get('ACCELA_'+environment+'_'+username+'_PASSWORD')
        scope = os.environ.get('ACCELA_SCOPE')

        self.accela.client.get_token(username, password, scope, environment)
    