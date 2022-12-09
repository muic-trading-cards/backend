from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.schema import *
from sqlalchemy import and_

transaction = Blueprint('transaction', __name__)

@transaction.route('/transaction/<transaction_id>', methods=["GET"])
@login_required
def view_transaction(transaction_id):
    session = Session()
    #make sure user belongs to the transaction
    transaction = session.query(Transaction).filter_by(id = transaction_id).first()
    listing_id = transaction.listing_id
    seller_id = session.query(Listing).filter_by(id = listing_id).first().owner_id
    buyer_id = transaction.buyer_id
    if seller_id != current_user.id and buyer_id != current_user.id:
        session.close()
        return redirect(url_for("transaction.display_transactions"))
    else:
        #return the listing
        listing = session.query(Listing).filter_by(id = listing_id).first()
        session.close()
        return render_template("view_transaction.html", transaction = transaction, listing = listing)


transaction.route('/transactions', methods=["GET"])
@login_required
def display_transactions():
    session = Session()
    #get all transactions for user
    transactions = session.query(Transaction).filter_by(buyer_id = current_user.id).all()
    sold_listings = session.query(Listing).filter_by(and_(owner_id = current_user.id, listing_status = status.sold)).all()
    for listing in sold_listings:
        transaction = session.query(Transaction).filter_by(listing_id = listing.id).first()
        transactions.append(transaction)
    session.close()
    return render_template("transactions.html", transactions = transactions)