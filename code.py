#!/usr/bin/env python

import webapp2
import logging
import json
import os
import random

from datetime import datetime, date, time
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from season import get_season
from photon import Photon
from google.appengine.api import memcache
from google.appengine.ext import deferred
from google.appengine.api import mail


log = logging.getLogger('webapp')

class Main(webapp2.RequestHandler):

    def get(self):

        photon = Photon()
        photon.get_bedroomtemp()
        current_temp =  memcache.get('current_temp') or 0

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

        self.message_generator()

        template_values = {
            'current_temp': current_temp,
            'message': message,
            'message_default': memcache.get('message_default')
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        
        contact_name = self.request.get('name')
        contact_email = self.request.get('email')
        contact_subject = "yeah its hot from %s" % (contact_name)
        contact_message = self.request.get('message') or memcache.get('message_default')
        message = mail.EmailMessage(sender="max@bedroomtemp-1015.appspotmail.com",
                            subject=contact_subject)
        message.to = "m.gelman08@gmail.com"
        message.body = contact_message + " from %s <%s> " % (contact_name, contact_email)
        message.send()
        self.redirect('/')
 
    def message_generator(self):
        messages = [
           "Its so hot in your house you could cook a turkey.",
           "Its so hot your furniture is melting.",
           "So hot your stuffed animals have applied for asylum in Abu Dhabi.",
           "Its hotter than India right now.",
           "The heat store called they are running out of heat.",
           "Make a dragon wanna retire, man."
        ]
        random_text = random.choice(messages)
        current_temp =  memcache.get('current_temp') or 0
        message = "Yo Peeps, its %s in your bedroom. %s" % (current_temp, random_text )
        if not memcache.get('message_default'):
            memcache.add('message_default', message)
        else:
            memcache.replace('message_default', message)

app = webapp2.WSGIApplication([('/', Main)], debug=True)


