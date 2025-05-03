from . import db
from datetime import datetime

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(100))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
