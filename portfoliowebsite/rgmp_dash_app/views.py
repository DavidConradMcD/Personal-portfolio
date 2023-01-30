from flask import render_template, request
from portfoliowebsite import rgmp_app

@rgmp_app.server.route('/rgmp_app/')
def rgmp_dashboard():
    return render_template('index.html.j2')
