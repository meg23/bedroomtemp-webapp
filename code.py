import webapp2
import logging
import json
import os

from datetime import datetime, date, time
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from helper import get_season

log = logging.getLogger('webapp')

class Temperature(db.Model):
    temp = db.IntegerProperty(required=True);
    date = db.DateTimeProperty(auto_now_add=True)

class User(db.model):
    email = db.StringProperty();
    authtoken = db.StringProperty();

class Rest(webapp2.RequestHandler):
    def post(self):
        temp = int(self.request.get('temp'))
        reading = Temperature(temp=temp)
        reading.put()

class Main(webapp2.RequestHandler):
    def get(self):
        tempQuery = db.GqlQuery("SELECT * FROM Temperature ORDER BY date DESC")
        last_entry = tempQuery.get()
        current_temp = last_entry.temp
        season = get_season(datetime.now())
        message = ""
        if current_temp < 65:
            message = "Pretty cool right now"
        elif season == "summer" and current_temp < 73 and current_temp > 65:
            message = "Pretty confortable right now"
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

app = webapp2.WSGIApplication([('/api.*', Rest), ('/', Main)], debug=True)

