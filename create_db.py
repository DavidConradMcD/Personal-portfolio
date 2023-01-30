from portfoliowebsite.models import Ratings
from portfoliowebsite import db
from portfoliowebsite import server

with server.app_context():
    db.create_all()
