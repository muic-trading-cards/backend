from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.schema import *

listing = Blueprint('listing', __name__)

@listing.route('/listing')
@login_required
def display_listing():
    session = Session()
    listings = session.query(Listing).filter_by(owner_id=current_user.id).all()
    session.close()
    return render_template('listing.html', listings=listings)
    
@listing.route('/create_listing',methods=["POST", "GET"])
@login_required
def create_listing():
    if request.method == 'GET':
        return render_template("add_listing.html")
    else:
        listing_name = request.form.get('listing_name')
        listing_description = request.form.get('listing_description')
        price = request.form.get('listing_price')
        image_url = request.form.get('listing_image')
        owner = current_user
        session = Session()
        new_listing = Listing(listing_name, listing_description, price, image_url, owner)
        session.add(new_listing)
        session.commit()
        session.close()
        return redirect(url_for("listing.display_listing"))
    


