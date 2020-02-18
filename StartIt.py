import requests
from urllib2 import HTTPError

WEB_SERVICE   = 'https://servicesv2.fleet2track.com//api/PLC/send'
MACHINERY_ID  = 'gelli-belloi_01'

class StartIt:

    def __init__(self, url=WEB_SERVICE):
        self.url = url


    def sendJson(self, msg):
        data = msg
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(self.url, data=json.dumps(data), headers=headers)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            #print('HTTP error occurred: ', http_err)  # Python 3.6
            return ('Send json - HTTP error occurred: ', http_err)  # Python 3.6
        except Exception as err:
            #print('Other error occurred:', err)  # Python 3.6
            return ('Send json - Other error occurred:', err)
        else:
            #print('Success!')
            return 'Send json: success'
