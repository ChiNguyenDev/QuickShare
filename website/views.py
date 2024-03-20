from dotenv import load_dotenv
# load env variables needed for Azure Vault
load_dotenv()

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from azure.storage.blob import BlobServiceClient
from .models import File
from . import db
import uuid
import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

secret_name = "connectionstring-quickshare"
credentials = ClientSecretCredential(
    client_id=os.environ['AZURE_CLIENT_ID'],
    tenant_id=os.environ['AZURE_TENANT_ID'],
    client_secret=os.environ['AZURE_CLIENT_SECRET']
)

secret_client = SecretClient(vault_url=os.environ['AZURE_VAULT_URL'], credential=credentials)
AZURE_CONNECTION_STRING = secret_client.get_secret(secret_name).value


views = Blueprint('views', __name__)

# Connect to Azure Storage
CONTAINER_NAME = 'container-quickshare'
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
@login_required
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            if request.content_length < 100 * 1024 * 1024:  # 100MB limit
                new_file = File(user_id=current_user.id, name=file.filename)
                db.session.add(new_file)
                db.session.commit()
                flash("File successfully uploaded", category="success")

                blob_name = f"uploads/{current_user.id}/{uuid.uuid4()}-{file.filename}"
                blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

                blob_client.upload_blob(file)

                flash('File successfully uploaded')
                return redirect(url_for('views.myFiles'))
            else:
                flash("File is too large", category="error")
        else:
            flash("No file selected", category="error")

    return redirect(url_for('views.home'))


