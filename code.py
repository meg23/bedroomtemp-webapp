#!/usr/bin/env python

import webapp2
import logging
import json
import os

from datetime import datetime, date, time
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from season import get_season
from photon import Photon
from google.appengine.api import memcache
from google.appengine.ext import deferred

log = logging.getLogger('webapp')

class Main(webapp2.RequestHandler):

    def get(self):

        photon = Photon()
        photon.get_bedroomtemp

        current_temp =  memcache.get('current_temp') or 0
        log.info("Got this temperature: %s" % current_temp)

        season = get_season(datetime.now())
        message = ""
        
        if current_temp == 0:
            message = "Yep, somethings broken over here"
        elif current_temp < 65 and current_temp != 0:
            message = "Pretty cool right now"
        elif season == "summer" and current_temp < 73 and current_temp > 65:
            message = "Pretty comfortable right now"
        elif season == "summer" and current_temp > 73 and current_temp < 80:
            message = "Starting to get warm here"
        elif current_temp >= 80:
            message = "Hotter Than a parking lot on Mars." 
        else:
            message = "Not sure what to make of the weather"

        template_values = {
            'current_temp': current_temp,
            'message': message
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([('/', Main)], debug=True)

