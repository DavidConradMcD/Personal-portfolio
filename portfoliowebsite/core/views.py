from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from portfoliowebsite.models import BlogPost


core = Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page',1,type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=3)
    return render_template('index.html.j2', blog_posts=blog_posts, page=page)

@core.route('/info')
def info():
    return render_template('info.html.j2')
