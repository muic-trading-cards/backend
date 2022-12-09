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
    #only apply this if the user is logged in

    session = Session()
    listings = session.query(Listing)\
                      .filter(Listing.listing_status == status.sell)\
                      .all()
    if len(listings) >= 9:
        listings = random.sample(listings, 9)
        listings_images = [session.query(Card)
                                  .filter(Card.id == listing.card_id)
                                  .one().card_image for listing in listings]

        new_listings = session.query(Listing)\
                              .filter(Listing.listing_status == status.sell)\
                              .order_by(Listing.created_at.asc())\
                              .limit(9)\
                              .all()
        new_listings_images = [session.query(Card)\
                              .filter(Card.id == listing.card_id)\
                              .one().card_image for listing in new_listings]

        latest_listings = [[new_listings[i:i+3], new_listings_images[i:i+3]] for i in range(0, len(new_listings), 3)]
        rand_listings = [[listings[i:i+3], listings_images[i:i+3]] for i in range(0, len(listings), 3)]
        return render_template('index.html', rand_listings=rand_listings, latest_listings=latest_listings, has_listings=True)
    else:
            return render_template('index.html', has_listings=False)

@main.route('/profile', methods=['GET'])
@login_required
def profile():
    pfp = default_profile_picture_url if current_user.profile_picture_url is None else current_user.profile_picture_url
    return render_template('profile.html', first_name=current_user.first_name, last_name=current_user.last_name, email=current_user.email, pfp_url=pfp)

@main.route('/about_us')
def about_us():
    return render_template('about_us.html')
