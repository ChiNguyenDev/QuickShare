# QuickShare

QuickShare is a Flask-based file-sharing website that allows users to easily upload and share files.

## Getting Started

Follow these steps to set up and run QuickShare:
1. **Configure Environment Variables**: 
    - Create an Azure Storage Account and Blob Container:
      - https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal
      - https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal
      
    - Store the Azure Blob Storage Connection String in Azure Key Vault:
      - https://learn.microsoft.com/en-us/azure/service-connector/tutorial-portal-key-vault?tabs=connectionstring

    
2. **Configure Environment Variables**: 
    - Create a `.env` file based on `.env.example`.
    - Add your Azure Client ID, Tenant ID, Client Secret, and Vault URL to the `.env` file.

    ```bash
    cp .env.example .env
    ```

3. **Build Docker Image**:
    - Build the Docker image using the provided Dockerfile.

    ```bash
    docker build -t quickshare ./QuickShare
    ```

4. **Run Docker Container**:
    - Run the Docker container, mapping port 80 of the host to port 80 of the container.

    ```bash
    docker container run -p 80:80 --name quickshare quickshare
    ```

5. **Access QuickShare**:
    - Open your web browser and navigate to `http://localhost` to access QuickShare.


6. **Troubleshooting**:
    If you encounter any issues during setup or while using QuickShare, here are a few tips:
    - Ensure all environment variables are correctly set in the .env file.
    - Check Docker container logs for any errors that may indicate issues with the connection to Azure services.
    - Verify that the Azure Blob Storage connection string stored in Azure Key Vault is correct and has the necessary permissions
