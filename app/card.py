from flask import Blueprint, render_template, redirect, url_for, request, flash,session
from flask_login import login_required, current_user
from app.schema import *
from app.obj_storage import upload_photo

card = Blueprint('card', __name__)

@card.route('/cards')
@login_required
def display_card():
    session = Session()
    cards_in_listings = session.query(Listing.card_id).filter_by(owner_id=current_user.id).all()
    all_cards = session.query(Card).filter_by(owner_id=current_user.id).all()
    cards_id_in_listing = [card[0] for card in cards_in_listings]
    cards = [card for card in all_cards if card.id not in cards_id_in_listing]
    session.close()
    return render_template('card.html', cards = cards)
    
@card.route('/create_card', methods=["POST", "GET"])
@login_required
def create_card():
    if request.method == "GET":
        session = Session()
        categories = session.query(Categories).all()
        return render_template("add_card.html", categories=categories)
    else:
        card_name = request.form.get('card_name')
        card_description = request.form.get('card_description')
        card_category_id = request.form.get('card_category')
        card_image = request.files['image']
        s3_url = upload_photo(card_image)
        owner = current_user
        
        dbsession = Session()
        card_category = dbsession.query(Categories).filter_by(id=card_category_id).first()
        new_card = Card(card_name, card_description, s3_url, owner, card_category)
        dbsession.add(new_card)
        dbsession.commit()

        dbsession.close()
        
        return redirect(url_for("card.display_card"))
    
@card.route('/view_card/<card_id>')
@login_required
def view_card(card_id):
    session = Session()
    card = session.query(Card).filter_by(id = card_id).first()
    category = session.query(Categories).filter_by(id = card.category_id).first()
    session.close()
    return render_template("view_card.html", card = card, category=category)
   