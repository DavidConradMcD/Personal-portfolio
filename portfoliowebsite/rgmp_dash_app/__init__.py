from flask import Flask
import dash
from flask import render_template_string
#from portfoliowebsite import app

def init_rgmp_dashboard(server):
    rgmp_app = dash.Dash(__name__, server=server, url_base_pathname='/esg_app/')
    from portfoliowebsite.rgmp_dash_app.rgmp_app import rgmp_app_layout

    rgmp_app.layout = rgmp_app_layout(rgmp_app)



    return rgmp_app.server

#rgmp_app = init_dashboard(app)

#from rgmp_dash_app import views
