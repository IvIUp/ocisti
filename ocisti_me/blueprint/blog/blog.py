from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ocisti_me.blueprint.auth import login_required
from ocisti_me.db_data.db_methods import get_db

bp_blog = Blueprint('blog', __name__)


@bp_blog.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN customer u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp_blog.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(blog_id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN customer u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (blog_id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {blog_id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp_blog.route('/<int:blog_id>/update', methods=('GET', 'POST'))
@login_required
def update(blog_id):
    print('test')
    post = get_post(blog_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, blog_id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp_blog.route('/<int:blog_id>/delete', methods=('POST',))
@login_required
def delete(blog_id):
    get_post(blog_id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (blog_id,))
    db.commit()
    return redirect(url_for('blog.index'))
