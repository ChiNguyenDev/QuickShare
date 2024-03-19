from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from azure.storage.blob import BlobServiceClient, BlobClient
from .models import File
from . import db
import uuid
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

views = Blueprint('views', __name__)

# Encryption with Key vault
key_vault_url = "https://keys-quickshare.vault.azure.net/"
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

AZURE_CONNECTION_STRING = secret_client.get_secret("keys-quickshare").value

# Connect to Azure Storage
CONTAINER_NAME = 'quickshare-storage'

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
            # check if a file was selected
            if file:
                # check if file is larger than 100mb(in Bytes)
                if request.content_length < 1000000:
                    new_file = File(user_id=current_user.id, name=file.filename)
                    db.session.add(new_file)
                    db.session.commit()
                    flash("File successfully uploaded", category="success")

                    # unique blob name with uuid to prevent overwrites
                    blob_name = f"uploads/{current_user.id}/{uuid.uuid4()}-{file.filename}"
                    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

                    blob_client.upload_blob(file)

                    flash('File successfully uploaded')

                    return redirect(url_for('views.myFiles'))
                else:
                    flash("File is too large", category="error")
                    return redirect(url_for('views.home'))
            else:
                flash("No file selected", category="error")
                return redirect(url_for('views.home'))

