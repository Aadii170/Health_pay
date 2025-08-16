# import os
# import tempfile
# from django.core.files.storage import Storage
# from django.conf import settings
# from django.core.files.base import ContentFile
# from supabase import create_client


# class SupabaseStorage(Storage):
#     """
#     Custom Django storage backend for Supabase Storage.

#     This allows Django to store uploaded files in a Supabase bucket instead of
#     the local filesystem.

#     Requirements:
#     - SUPABASE_URL, SUPABASE_KEY, and SUPABASE_BUCKET must be set in settings.py
#     - Supabase bucket must have Row-Level Security (RLS) policies that allow uploads.
#     """

#     def __init__(self):
#         # Create a Supabase client using credentials from Django settings
#         self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
#         self.bucket = settings.SUPABASE_BUCKET

#     def _save(self, name, content):
#         """
#         Save a file to Supabase Storage.

#         Django calls this method internally when saving files.
#         - `name` is the desired path/filename in the storage bucket.
#         - `content` is a Django UploadedFile object (can be in-memory or temp file).

#         Supabase's Python SDK expects a file path or raw bytes,
#         so we write the file content into a temporary file, then upload that file.
#         """
#         # Create a temporary file and write the file's content into it
#         with tempfile.NamedTemporaryFile(delete=False) as tmp:
#             tmp.write(content.read())  # Read the uploaded content as bytes
#             tmp_path = tmp.name        # Store the temp file path

#         # Upload the temporary file to the Supabase bucket
#         self.client.storage.from_(self.bucket).upload(
#             name,                # Destination filename/path in Supabase
#             tmp_path,            # Local file path to upload
#             {"cacheControl": "3600"}  # Optional: browser cache time in seconds
#         )

#         return name  # Django stores this as the saved file's name

#     def _open(self, name, mode="rb"):
#         """
#         Retrieve a file from Supabase Storage.

#         Django calls this when opening a stored file.
#         - `name` is the file path in the Supabase bucket.
#         - Returns a Django ContentFile object containing the file's data.
#         """
#         res = self.client.storage.from_(self.bucket).download(name)  # Get file bytes
#         return ContentFile(res)

#     def exists(self, name):
#         """
#         Check if a file exists in the Supabase bucket.

#         - Returns True if the file is found, False otherwise.
#         """
#         try:
#             files = self.client.storage.from_(self.bucket).list(path="")  # List all files
#             return any(f["name"] == name for f in files)  # Look for a matching filename
#         except Exception:
#             return False

#     def url(self, name):
#         """
#         Get the public URL for a file stored in Supabase.

#         This works only if the Supabase bucket is public or has a public access policy.
#         """
#         return self.client.storage.from_(self.bucket).get_public_url(name)

import mimetypes
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from supabase import create_client


class SupabaseStorage(Storage):
    """
    Django storage backend for Supabase public bucket "media".
    Handles PDFs and other files with correct MIME types.
    """

    def __init__(self):
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket = "media"  # Your bucket name

    def _save(self, name, content):
        content.seek(0)
        file_bytes = content.read()  # Read as bytes

        # Detect MIME type
        if name.lower().endswith('.pdf'):
            content_type = "application/pdf"
        else:
            content_type, _ = mimetypes.guess_type(name)
            if not content_type:
                content_type = "application/octet-stream"

        # Upload to Supabase with correct file_options
        response = self.client.storage.from_(self.bucket).upload(
            path=name,
            file=file_bytes,
            file_options={
                "content-type": content_type,  # ✅ correct key
                "cache-control": "3600",
                "upsert": "true"
            }
        )

        if "error" in str(response).lower():
            raise Exception(f"Upload failed: {response}")

        return name

    def _open(self, name, mode="rb"):
        file_bytes = self.client.storage.from_(self.bucket).download(name)
        return ContentFile(file_bytes)

    def exists(self, name):
        try:
            files = self.client.storage.from_(self.bucket).list(path="")
            return any(f["name"] == name for f in files)
        except Exception:
            return False

    def url(self, name):
        return self.client.storage.from_(self.bucket).get_public_url(name)
