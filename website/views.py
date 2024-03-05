from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from azure.storage.blob import BlobServiceClient, BlobClient
from .models import File
from . import db
import os

views = Blueprint('views', __name__)

# Connect to Azure Storage
AZURE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=quickshareproject2024;AccountKey=u8U0C0YlHt4lzm2wc1hW5GFepqKutDT9WNelPBuhujz39BPpxyX1eNr0NPPH1LbI35s97FToFuRq+AStQhuOTg==;EndpointSuffix=core.windows.net'
CONTAINER_NAME = 'quicksharestorage'

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

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

                # Create a unique "smart" name for the blob to avoid overwrites
                blob_name = "uploads/{filename}".format(filename=file.filename)
                blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

                # Upload the file
                blob_client.upload_blob(file)

                flash('File successfully uploaded')

                return redirect(url_for('views.myFiles'))
            else:
                flash("No file selected", category="error")
                return redirect(url_for('views.home'))

