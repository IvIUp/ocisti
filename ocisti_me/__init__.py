import os
from flask import Flask
from .db_data import db_methods
from .blueprint import auth, blog

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'ocisti_me.sqlite'),
)

db_methods.init_app(app)
app.register_blueprint(auth.bp_auth)
app.register_blueprint(blog.bp_blog)
app.add_url_rule('/', endpoint='index')