
import aiohttp

from pathlib import Path
from .types.attachment import Attachment as AttachmentPayload


class Attachment:

    def __init__(self, data: AttachmentPayload) -> None:
        self.url: str = data['url']
        self.name: str = data['name']
        self.file_size_bytes: int = data['fileSiteBytes']
        self._formdata: aiohttp.FormData = None

    @classmethod
    def builder(cls, file_path: str):
        self = cls.__new__(cls)

        self.file_path = Path(file_path)

        if not self.file_path.exists() or not self.file_path.is_file():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        form = aiohttp.FormData()
        form.add_field(
            name="image",
            value=self.file_path.open('rb'),
            filename=self.file_path.name,
            content_type="application/octet_stream"
        )
        form.add_field('type', "attachment")

        self.name = self.file_path.name
        self.file_size_bytes = self.file_path.stat().st_size
        self._formdata = form
        return self

    def to_dict(self):
        return {
            "url": self.url,
            "name": self.name,
            "fileSizeBytes": self.file_size_bytes
        }
