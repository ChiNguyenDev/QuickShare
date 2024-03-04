from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import File
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/myfiles')
@login_required
def myFiles():
    return render_template("file.html", user=current_user)


@views.route('/upload', methods=['POST'])
def upload_file():
    if request.method == "POST":
        if current_user.is_authenticated:
            file = request.files["file"]
            if file:
                new_file = File(user_id=current_user.id, name=file.filename)
                db.session.add(new_file)
                db.session.commit()
                flash("File successfully uploaded", category="success")
                return redirect(url_for('views.myFiles'))
            else:
                flash("No file selected", category="error")
                return redirect(url_for('views.home'))

