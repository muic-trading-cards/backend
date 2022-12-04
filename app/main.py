import random
from flask import Flask, Blueprint, render_template
from flask_login import login_required, current_user
from app.schema import *
from app.base import *
from app.shared import default_profile_picture_url

main = Blueprint('main', __name__)
Base.metadata.create_all(Engine)


@main.route('/', methods=['GET'])
def index():
    session = Session()
    listings = random.sample(session.query(Listing).all(), 3)
    new_listings = session.query(Listing).order_by(Listing.created_at.asc()).limit(9).all()

    latest_listings = [listings[i:i+3] for i in range(0, len(new_listings), 3)]
    rand_listings = [listings[i:i+3] for i in range(0, len(listings), 3)]
    return render_template('index.html', rand_listings=rand_listings, latest_listings=latest_listings)

@main.route('/profile', methods=['GET'])
@login_required
def profile():
    pfp = default_profile_picture_url if current_user.profile_picture_url is None else current_user.profile_picture_url
    return render_template('profile.html', first_name=current_user.first_name, last_name=current_user.last_name, email=current_user.email, pfp_url=pfp)
