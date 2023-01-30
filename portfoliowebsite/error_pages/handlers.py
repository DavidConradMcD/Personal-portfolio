# Going to serve the views of our particular error pages

from flask import Blueprint, render_template

error_pages = Blueprint('error_pages', __name__)

# There are other html codes we can pass to Flask's errorhandler
@error_pages.app_errorhandler(404)
def error_404(error):
    # This returns a tuple, first part is the render template, second part
    # is the 404 code
    return render_template('error_pages/404.html.j2'), 404
