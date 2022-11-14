from flask import Flask, Blueprint, render_template
from flask_login import login_required, current_user
from app.schema import *
from app.base import *

main = Blueprint('main', __name__)
Base.metadata.create_all(Engine)


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', first_name=current_user.first_name, last_name=current_user.last_name)
