from django.apps import AppConfig

from CVServer.geosample_model import load_model

class CvserverConfig(AppConfig):    
    name = 'CVServer'

    def ready(self):
        load_model()