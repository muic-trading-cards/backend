from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.schema import *

listing = Blueprint('listing', __name__)

@listing.route('/listing')
@login_required
def display_listing():
    categories_dict = {}
    session = Session()
    listings = session.query(Listing).filter_by(owner_id=current_user.id, listing_status=status.sell).all()
    cards_in_listings = session.query(Listing.card_id).filter_by(owner_id=current_user.id).all()
    cards_id_in_listing = [card[0] for card in cards_in_listings]
    card_images_and_categories = {}
    #making a dictionary of card_id_in_listing and card_image
    for card_ids in cards_id_in_listing:
        card = session.query(Card).filter_by(id=card_ids).first()
        card_images_and_categories[card_ids] = (card.card_image, card.category_id)
    #making a dictionary of category_id and catagory_name
    categories = session.query(Categories).all()
    for category in categories:
        categories_dict[category.id] = category.category_name
    session.close()
    return render_template('listing.html', listings=listings, card_images_and_categories=card_images_and_categories, categories_dict=categories_dict)
    
@listing.route('/explore', methods = ['GET'])
def explore():
    session = Session()
    listings = session.query(Listing).filter_by(listing_status=status.sell).all()
    cards_in_listings = session.query(Listing.card_id).filter_by(listing_status=status.sell).all()
    cards_id_in_listing = [card[0] for card in cards_in_listings]
    card_images = {}
    for card_ids in cards_id_in_listing:
        card = session.query(Card).filter_by(id=card_ids).first()
        card_images[card_ids] = card.card_image
    session.close()
    return render_template('explore.html', listings=listings, card_images=card_images)
    

@listing.route('/create_listing/<card_id>',methods=["POST", "GET"])
@login_required
def create_listing(card_id):
    if request.method == 'GET':
        if card_id:
            session = Session()
            selling_card = session.query(Card).filter_by(id=card_id).first()
            #check to make sure this card is owned by the owner
            if selling_card.owner_id != current_user.id:
                flash("You do not own this card")
                return redirect(url_for('card.displaycard'))
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
    card = session.query(Card).filter_by(id = listing.card_id).first()
    card_image = card.card_image
    session.close
    return render_template("view_listing.html", listing=listing, card_image=card_image)
   
@listing.route('/buy_listing/<listing_id>', methods=["POST"])
@login_required
def buy_listing(listing_id):
    #get the current listing and check the price
    session = Session()

    listing = session.query(Listing).filter_by(id = listing_id).first()
    #get the current user's balance
    card = session.query(Card).filter_by(id = listing.card_id).first()
    buyer = session.query(User).filter_by(id = current_user.id).first()
    seller = session.query(User).filter_by(id = listing.owner_id).first()
    balance = buyer.wallet_balance
    price = listing.listing_price
    #check if the user has enough balance
    if listing.listing_status == status.sell and balance >= price:
        transaction = Transaction(buyer_id=buyer.id, 
        listing_id=listing.id, transaction_price=price)
        session.add(transaction)
        listing.listing_status = status.sold
        #if yes, deduct the balance and add the card to the user's collection

        new_balance = balance - price
        buyer.wallet_balance = new_balance
        seller.wallet_balance = seller.wallet_balance + price

        card.owner_id = buyer.id
        session.commit()
        session.close()
        flash("You have successfully bought the card")
        return redirect(url_for("card.display_card"))
    else:
        flash("You do not have enough money to buy this card or card has sold already")
        return redirect(url_for("listing.display_listing"))
        
@listing.route('/search', methods=['POST'])
@login_required
def search():
    query = request.form.get('search') 
    session = Session()
    listings = session.query(Listing).filter(Listing.listing_status == status.sell, Listing.listing_name.match(f"%{query}%")).all()
    cards_in_listings = session.query(Listing.card_id).filter_by(listing_status=status.sell).all()
    cards_id_in_listing = [card[0] for card in cards_in_listings]
    card_images = {}
    for card_ids in cards_id_in_listing:
        card = session.query(Card).filter_by(id=card_ids).first()
        card_images[card_ids] = card.card_image
    session.close()
    return render_template('search-results.html', results=listings, card_images=card_images)

@listing.route('/delete_listing/<listing_id>', methods = ['POST'])
@login_required
def delete_listing(listing_id):
    #ensure listing is owned by current user and still active
    session = Session()
    listing = session.query(Listing).filter_by(id = listing_id).first()
    if listing.owner_id == current_user.id and listing.listing_status == status.sell:
        session.delete(listing)
        session.commit()
        session.close()
        return redirect(url_for("listing.display_listing"))
    else:
        return redirect(url_for("listing.display_listing"))


@listing.route('/edit_listing/<listing_id>', methods = ['GET', 'POST'])
@login_required
def edit_listing(listing_id):
    if request.method == 'GET':
        session = Session()
        listing = session.query(Listing).filter_by(id = listing_id).first()
        session.close()
        if listing.owner_id == current_user.id and listing.listing_status == status.sell:
            return render_template('edit_listing.html', listing=listing, lid=listing_id)
        else:
            return redirect(url_for("listing.display_listing"))
    else:
        session = Session()
        listing = session.query(Listing).filter_by(id = listing_id).first()
        if listing.owner_id == current_user.id and listing.listing_status == status.sell:
            listing.listing_name = request.form.get('listing_name')
            listing.listing_description = request.form.get('listing_description')
            listing.listing_price = request.form.get('listing_price')
            session.commit()
            session.close()
            return redirect(url_for("listing.display_listing"))
        else:
            return redirect(url_for("listing.display_listing"))