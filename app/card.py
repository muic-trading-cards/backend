from flask import Blueprint, render_template, redirect, url_for, request, flash,session
from flask_login import login_required, current_user
from app.schema import *

card = Blueprint('card', __name__)

@card.route('/cards')
@login_required
def display_card():
    session = Session()
    cards = session.query(Card).filter_by(owner_id=current_user.id).all()
    session.close()
    return render_template('card.html', cards = cards)
    
@card.route('/create_card', methods=["POST", "GET"])
@login_required
def create_card():
    if request.method == "GET":
        return render_template("add_card.html")
    else:
        card_name = request.form.get('card_name')
        card_description = request.form.get('card_description')
        owner = current_user

        dbsession = Session()
        new_card = Card(card_name, card_description, owner)
        dbsession.add(new_card)
        dbsession.commit()

        dbsession.close()
        
        flash('Added card success')

        return redirect(url_for("card.display_card"))
    
@card.route('/view_card/<card_id>')
@login_required
def view_card(card_id):
    session = Session()
    card = session.query(Card).filter_by(id = card_id).first()
    session.close()
    return render_template("view_card.html", card = card)
   
    


