from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.schema import *

card = Blueprint('card', __name__)

@card.route('/cards')
@login_required
def display_card():
    return render_template('card.html')
    
@card.route('/create_card', methods=["POST", "GET"])
@login_required
def create_card():
    if request.method == "GET":
        return render_template("add_card.html")
    else:
        card_name = request.form.get('card_name')
        card_description = request.form.get('card_description')
        owner = current_user

        session = Session()
        new_card = Card(card_name, card_description, owner)
        session.add(new_card)
        session.commit()

        session.close()
        
        flash('Added card success')

        return redirect(url_for("card.display_card"))
    


