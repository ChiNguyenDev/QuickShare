# QuickShare

QuickShare is a Flask-based file-sharing website that allows users to easily upload and share files.

## Getting Started

Follow these steps to set up and run QuickShare:

1. **Configure Environment Variables**: 
    - Create a `.env` file based on `.env.example`.
    - Add your Azure Client ID, Tenant ID, Client Secret, and Vault URL to the `.env` file.

    ```bash
    cp .env.example .env
    ```

2. **Build Docker Image**:
    - Build the Docker image using the provided Dockerfile.

    ```bash
    docker build -t quickshare ./QuickShare
    ```

3. **Run Docker Container**:
    - Run the Docker container, mapping port 80 of the host to port 80 of the container.

    ```bash
    docker container run -p 80:80 --name quickshare quickshare
    ```

4. **Access QuickShare**:
    - Open your web browser and navigate to `http://localhost` to access QuickShare.
