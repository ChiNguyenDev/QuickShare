from dotenv import load_dotenv
# load env variables needed for Azure Vault
load_dotenv()

from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, abort
from flask_login import login_required, current_user
from azure.storage.blob import BlobServiceClient
from .models import File
from . import db
import uuid  # generate unique identifiers
import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import io


# authenticate against azure services for access
credentials = ClientSecretCredential(
    client_id=os.environ['AZURE_CLIENT_ID'],
    tenant_id=os.environ['AZURE_TENANT_ID'],
    client_secret=os.environ['AZURE_CLIENT_SECRET']
)
# access key vault
secret_client = SecretClient(vault_url=os.environ['AZURE_VAULT_URL'], credential=credentials)
# retrieve connection string with the name of the secret
AZURE_CONNECTION_STRING = secret_client.get_secret("connectionstring-quickshare").value

views = Blueprint('views', __name__)

CONTAINER_NAME = 'container-quickshare'
# manage / interact with the blob storage
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
# container_client: upload, download or manage blobs
container_client = blob_service_client.get_container_client(CONTAINER_NAME)  # container name


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")



@views.route('/myfiles')
@login_required
def myFiles():
    return render_template("file.html", user=current_user)


@views.route('/upload', methods=['POST'])
def upload_file():
    # if POST: retrieve file
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            if request.content_length < 100 * 1024 * 1024:  # 100MB limit
                flash("File successfully uploaded", category="success")
                # generate unique blob name

                unique_id = uuid.uuid4()
                print(unique_id)
                blob_name = f"uploads/{unique_id}-{file.filename}"
                blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
                blob_client.upload_blob(file)

                new_file = File(name=file.filename, unique_id=str(unique_id),
                                blob_name=blob_name)

                if current_user.is_authenticated:
                    new_file.user_id = current_user.id

                db.session.add(new_file)
                db.session.commit()

                flash('File successfully uploaded')
                return redirect(url_for('views.download_page', unique_id=str(unique_id)))
            else:
                flash("File is too large", category="error")
        else:
            flash("No file selected", category="error")

    return redirect(url_for('views.home'))


@views.route('/download/<unique_id>')
def download_file(unique_id):
    # Retrieve the file entry from the database
    file_entry = File.query.filter_by(unique_id=unique_id).first()
    if not file_entry:
        abort(404, description="File not found")

    # Get the blob client for the file
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_entry.blob_name)

    # Download the file contents
    blob_data = blob_client.download_blob().readall()

    # Create a response with the file data
    return send_file(io.BytesIO(blob_data), as_attachment=True, download_name=file_entry.name)


@views.route('/download_page/<unique_id>')
def download_page(unique_id):
    file_entry = File.query.filter_by(unique_id=unique_id).first()
    if not file_entry:
        abort(404, description="File not found")

    return render_template('download_page.html', file_name=file_entry.name,
                           download_url=url_for('views.download_file', unique_id=unique_id))


