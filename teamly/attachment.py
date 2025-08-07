'''
MIT License

Copyright (c) 2025 Fatih Kuloglu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

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
