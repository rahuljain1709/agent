import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

class GDriveUploader:
    def __init__(self, credentials_json, folder_id=None):
        creds = service_account.Credentials.from_service_account_file(
            credentials_json,
            scopes=["https://www.googleapis.com/auth/drive.file"]
        )
        self.drive = build("drive", "v3", credentials=creds)
        self.folder_id = folder_id

    def upload_bytes(self, data, filename):
        media = MediaIoBaseUpload(
            io.BytesIO(data),
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        meta = {"name": filename}
        if self.folder_id:
            meta["parents"] = [self.folder_id]

        file = self.drive.files().create(
            body=meta,
            media_body=media,
            fields="id"
        ).execute()

        return file.get("id")
