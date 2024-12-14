import requests
import logging

class ContentUploadAdapter:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    def upload_content(self, files, content_type):
        url = f"{self.base_url}/upload"
        self.logger.info(f"Uploading content to {url} with type {content_type}")

        files_payload = [('files', (file.filename, file.read())) for file in files]
        data_payload = {'type': content_type}

        response = requests.post(url, files=files_payload, data=data_payload)
        if response.status_code != 200:
            self.logger.error(f"Failed to upload content: {response.text}")
            raise Exception(f"Content upload failed: {response.status_code} - {response.text}")

        return response.json()

    def retrieve_content(self, file_name):
        url = f"{self.base_url}/download/{file_name}"
        self.logger.info(f"Retrieving content from {url}")

        response = requests.get(url)
        if response.status_code != 200:
            self.logger.error(f"Failed to retrieve content: {response.text}")
            raise Exception(f"Content retrieval failed: {response.status_code} - {response.text}")

        return response.content
