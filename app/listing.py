from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.schema import *

listing = Blueprint('listing', __name__)

@listing.route('/listing')
@login_required
def display_listing():
    session = Session()
    listings = session.query(Listing).filter_by(owner_id=current_user.id).all()
    cards_in_listings = session.query(Listing.card_id).filter_by(owner_id=current_user.id).all()
    cards_id_in_listing = [card[0] for card in cards_in_listings]
    card_images = {}
    for card_ids in cards_id_in_listing:
        card = session.query(Card).filter_by(id=card_ids).first()
        card_images[card_ids] = card.card_image
    session.close()
    return render_template('listing.html', listings=listings, card_images=card_images)
    
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
            card_image = selling_card.card_image
            session.close()
            return render_template("add_listing.html", cid=cid, card_name=card_name, card_description=card_description, card_image=card_image)
        else:
            flash("Please create listing by clicking sell on the card page")
            return redirect(url_for('card.displaycard'))
    else:
        if card_id:
            listing_name = request.form.get('listing_name')
            listing_description = request.form.get('listing_description')
            price = request.form.get('listing_price')
            owner = current_user
            session = Session()
            selling_card = session.query(Card).filter_by(id=card_id).first()
            new_listing = Listing(listing_name, listing_description, price, owner, selling_card)
            session.add(new_listing)
            session.commit()
            session.close()
        else:
            flash("Please create listing by clicking sell on the card page")
            return redirect(url_for('card.displaycard'))
        return redirect(url_for("listing.display_listing"))

@listing.route('/view_listing/<listing_id>')
@login_required
def view_listing(listing_id):
    session = Session()
    listing = session.query(Listing).filter_by(id = listing_id).first()
    listings = session.query(Listing).filter_by(owner_id=current_user.id).all()
    cards_in_listings = session.query(Listing.card_id).filter_by(owner_id=current_user.id).all()
    cards_id_in_listing = [card[0] for card in cards_in_listings]
    card_images = {}
    for card_ids in cards_id_in_listing:
        card = session.query(Card).filter_by(id=card_ids).first()
        card_images[card_ids] = card.card_image
    session.close
    return render_template("view_listing.html", listing=listing, card_images=card_images)
   
    


