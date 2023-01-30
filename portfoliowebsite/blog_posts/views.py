from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from portfoliowebsite import db
from portfoliowebsite.models import BlogPost
from portfoliowebsite.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts',__name__)

# CREATE
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(title = form.title.data,
                            text= form.text.data,
                            user_id= current_user.id)

        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')

        return redirect(url_for('core.index'))

    return render_template('create_post.html.j2', form=form)




# VIEW
# someone can input the blog post ID and find that single blog post
# the int: makes sure that blog_post_id is treated as an integer inside our function
# if you don't pass int sqlalchemy thinks that this is a string so query doesn't work
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html.j2', title=blog_post.title,
                                                date = blog_post.date,
                                                post=blog_post)



# UPDATE
@blog_posts.route('/<int:blog_post_id>/update', methods=['GET','POST'])
@login_required
def update(blog_post_id):
    # Check if blog post exists if not throw 404 error
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    # Check to see person visiting this blog post is the author
    if blog_post.author != current_user:
        # abort is a function Flask comes with which lets you pass in error codes
        abort(403)

    # This lets them fill out the blog post update form
    form = BlogPostForm()

    if form.validate_on_submit():

        # Just reset title and text to what's entered in the form
        blog_post.title = form.title.data
        blog_post.text = form.text.data

        db.session.commit()
        flash('Blog Post Updated')

        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))

    # This is to make sure that the original post title and text shows
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html.j2', title='Updating', form=form)



# DELETE
# We're not going to have a delete.html we'll have a button that executes this code
@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):
    # Check if blog post exists if not throw 404 error
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    # Check to see person visiting this blog post is the author
    if blog_post.author != current_user:
        # abort is a function Flask comes with which lets you pass in error codes
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog post deleted')

    return redirect(url_for('core.index'))
