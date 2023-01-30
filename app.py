#This imports app from __init__.py
#So when we say from ratingswebsite its pulling from __init__.py
from portfoliowebsite import server
from portfoliowebsite.models import User
from portfoliowebsite.models import Ratings
from portfoliowebsite import db
import numpy as np
#from rgmp_dash_app import init_dashboard

#app = init_app(app)

server.app_context().push()

#rgmp_app = init_dashboard(app)


#from rgmp_dash_app import rgmp_app
'''from portfoliowebsite.rgmp_dash_app import create_dash_application
rgmp_app = create_dash_application(app)'''

if __name__ == '__main__':
    server.run(debug=True)
