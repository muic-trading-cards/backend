from flask import Blueprint, render_template, redirect, url_for, request, flash,session
from flask_login import login_required, current_user
from app.schema import *
from app.obj_storage import upload_photo

card = Blueprint('card', __name__)

@card.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@card.route('/cards')
@login_required
def display_card():
    session = Session()
    categories_dict = {}
    cards_in_listings = session.query(Listing.card_id).filter_by(owner_id=current_user.id, listing_status = status.sell).all()
    all_cards = session.query(Card).filter_by(owner_id=current_user.id).all()
    cards_id_in_listing = [card[0] for card in cards_in_listings]
    cards = [card for card in all_cards if card.id not in cards_id_in_listing]
    categories = session.query(Categories).all()
    for category in categories:
        categories_dict[category.id] = category.category_name

    session.close()
    return render_template('card.html', cards = cards, categories_dict = categories_dict)
    
@card.route('/create_card', methods=["POST", "GET"])
@login_required
def create_card():
    if request.method == "GET":
        session = Session()
        categories = session.query(Categories).all()
        categories = categories[3:] #remove legacy categories that are no longer used
        session.close()
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
    
#this is an error case
@card.route('/view_card/')
def view_card_err():
    return render_template("404.html")

@card.route('/view_card/<card_id>')
@login_required
def view_card(card_id):
    session = Session()
    card = session.query(Card).filter_by(id = card_id).first()
    category = session.query(Categories).filter_by(id = card.category_id).first()
    listing = session.query(Listing).filter_by(card_id = card_id).order_by(Listing.id.desc()).first()
    listing_status = 0
    if listing != None and current_user.id == listing.owner_id:
        listing_status = listing.listing_status.value

    session.close()
    print(card)
    if card == None:
        return render_template("404.html")
    return render_template("view_card.html", card = card, category=category, listing_status=listing_status)

@card.route('/edit_card/<card_id>', methods=["POST", "GET"])
@login_required
def edit_card(card_id):
    if(request.method == 'GET'):
        session = Session()
        card = session.query(Card).filter_by(id = card_id).first()
        category = session.query(Categories).filter_by(id = card.category_id).first()
        categories = session.query(Categories).all()
        session.close()
        return render_template("edit_card.html", card = card, categories=categories, category=category)
    else:
        session = Session()
        card = session.query(Card).filter_by(id = card_id).first()
        card_name = request.form.get('card_name')
        card_description = request.form.get('card_description')
        card_category_id = request.form.get('card_category')
        if card_name:
            card.card_name = card_name
        if card_description:
            card.card_description = card_description
        card.category_id = card_category_id
        if request.files['image']:
            card_image = request.files['image']
            s3_url = upload_photo(card_image)
            card.card_image = s3_url
        session.commit()
        session.close()
        return redirect(url_for("card.display_card"))

   

@card.route('/delete_card/<card_id>', methods=["POST"])
@login_required
def delete_card(card_id):
    #make sure the owner owns the card they're trying to delete
    session = Session()
    card = session.query(Card).filter_by(id = card_id).first()
    if card.owner_id == current_user.id:
        session.delete(card)
        session.commit()
        session.close()
        return redirect(url_for("card.display_card"))
    else:
        session.close()
        return redirect(url_for("card.display_card"))