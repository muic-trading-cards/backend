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
    
@listing.route('/create_listing/<card_id>',methods=["POST", "GET"])
@login_required
def create_listing(card_id):
    if request.method == 'GET':
        if card_id:
            session = Session()
            selling_card = session.query(Card).filter_by(id=card_id).first()
            cid = selling_card.id
            card_name = selling_card.card_name
            card_description = selling_card.card_description
            session.close()
            return render_template("add_listing.html", cid=cid, card_name=card_name, card_description=card_description)
        else:
            flash("Please create listing by clicking sell on the card page")
            return redirect(url_for('card.displaycard'))
    else:
        if card_id:
            listing_name = request.form.get('listing_name')
            listing_description = request.form.get('listing_description')
            price = request.form.get('listing_price')
            image_url = request.form.get('listing_image')
            owner = current_user
            session = Session()
            selling_card = session.query(Card).filter_by(id=card_id).first()
            new_listing = Listing(listing_name, listing_description, price, image_url, owner, selling_card)
            session.add(new_listing)
            session.commit()
            session.close()
        else:
            flash("Please create listing by clicking sell on the card page")
            return redirect(url_for('card.displaycard'))
        return redirect(url_for("listing.display_listing"))
    


