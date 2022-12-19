import functools
from ocisti_me.db_data.db_methods import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_auth.route('/register_cleaner', methods=('GET', 'POST'))
def register_cleaner():
    if request.method == 'POST':
        db = get_db()
        error = None

        username = request.form['username']
        password = request.form['password']
        if 'availability' in request.form:
            availability = request.form['availability']
        if 'birth_date' in request.form:
            birth_date = request.form['birth_date']
        if 'location' in request.form:
            location = request.form['location']
        if 'description' in request.form:
            description = request.form['description']

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO cleaner (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"{username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register_cleaner.html')


@bp_auth.route('/register_customer', methods=('GET', 'POST'))
def register_customer():
    if request.method == 'POST':
        db = get_db()
        error = None
        username = request.form['username']
        password = request.form['password']

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO customer (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"{username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register_customer.html')


@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None
        if 'cleaner' in request.form:
            user_type = 'cleaner'
            user = db.execute(
                'SELECT * FROM cleaner WHERE username = ?', (username,)
            ).fetchone()
        else:
            user_type = 'customer'
            user = db.execute(
                'SELECT * FROM customer WHERE username = ?', (username,)
            ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_type'] = user_type
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp_auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    if user_id is None:
        g.user = None
    else:
        statement = f"SELECT * FROM {user_type} WHERE id = {user_id}"
        g.user = get_db().execute(statement).fetchone()


@bp_auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
