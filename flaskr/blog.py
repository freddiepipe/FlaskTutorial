from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT * FROM post JOIN user ON post.author_id = user.id ORDER BY created DESC').fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'You must provide a title for your post'
        elif not body:
            error = 'You must provide some content for the post'

        if error is None:
            db = get_db()
            db.execute('INSERT INTO post (author_id, title, body) VALUES (?, ?, ?)',
                       (g.user['id'], title, body))
            db.commit()
            return redirect(url_for('blog.index'))

        flash(error)

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT * FROM post join user on post.author_id = user.id where post.id = ?', (id,)).fetchone()
    if post is None:
        abort(404, "Post id {} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'You must provide a title for your post'
        elif not body:
            error = 'You must provide some content for the post'

        if error is None:
            db = get_db()
            db.execute(
                'UPDATE POST SET title = ?, body = ? WHERE id = ?', (title, body, id))
            db.commit()
            return redirect(url_for('blog.index'))
        flash(error)

    return render_template('blog/update.html', post=post)


@bp.route('/myprofile')
def profile():
    db = get_db()
    posts = db.execute(
        'SELECT * FROM post JOIN user ON post.author_id = user.id WHERE author_id = ? ORDER BY created DESC', (g.user['id'],)).fetchall()
    return render_template('blog/profile.html', posts=posts)
