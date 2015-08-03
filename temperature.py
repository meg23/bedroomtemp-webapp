from google.appengine.ext import db

class Temperature(db.Model):
    temp = db.IntegerProperty(required=True);
    date = db.DateTimeProperty(auto_now_add=True)
