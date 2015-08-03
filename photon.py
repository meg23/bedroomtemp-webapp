
import webapp2
import json
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from secrets import DEVICE_ID, ACCESS_TOKEN

class Photon():
    
    def get_bedroomtemp(self):

        '''
        Fetch temperature data from photon cloud
        '''

        base = "https://api.particle.io/v1/devices"
        rpc = urlfetch.create_rpc()
        urlfetch.make_fetch_call(rpc, 
            "%s/%s/bedroom_temp?access_token=%s" % ( base, DEVICE_ID, ACCESS_TOKEN))

        try:

            result = rpc.get_result()
            json_string = result.content
            data = json.loads(json_string)
            core_info =  data["coreInfo"]
            temp = int(data["result"])

            if not memcache.get('current_temp'):
               memcache.add('current_temp', temp)

            else:
               memcache.replace('current_temp', temp)
               

        except urlfetch.DownloadError:
            logging.error("Failed download the data from the photon cloud") 

