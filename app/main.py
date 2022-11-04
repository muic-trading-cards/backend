from flask import Flask, Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from app.shared import *

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')
