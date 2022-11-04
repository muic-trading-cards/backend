from flask import Flask, Blueprint, render_template
from app.schema import *
from app.base import *

main = Blueprint('main', __name__)
Base.metadata.create_all(Engine)


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')
