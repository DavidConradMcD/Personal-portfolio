from flask import Flask
import dash
from flask import render_template_string
#from portfoliowebsite import app

def init_jobs_dashboard(server):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    jobs_app = dash.Dash(__name__, server=server, url_base_pathname='/jobs_app/', external_stylesheets=external_stylesheets)
    jobs_app.config.suppress_callback_exceptions = True
    from portfoliowebsite.job_postings_dash_app.job_postings_app import jobs_app_layout

    jobs_app.layout = jobs_app_layout(jobs_app)



    return jobs_app.server
