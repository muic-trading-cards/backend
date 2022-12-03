from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.schema import *

listing = Blueprint('listing', __name__)

@listing.route('/listing')
@login_required
def display_listing():
    return render_template('listing.html')
    
@listing.route('/create_listing',methods=["POST", "GET"])
@login_required
def create_listing():
    if request.method == "GET":
        return render_template("add_listing.html")
    else:
        return redirect(url_for("display_listing"))
    


