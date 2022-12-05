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

@listing.route('/view_listing/<listing_id>')
@login_required
def view_listing(listing_id):
    session = Session()
    listing = session.query(Listing).filter_by(id = listing_id).first()
    session.close
    return render_template("view_listing.html", listing=listing)
   
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
        