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
import json


from datetime import datetime
from typing import Union, Dict, Any


class _MissingSentinel:

    __slots__ = ()

    def __eq__(self, value: object, /) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self) -> str:
        return '...'

MISSING: Any = _MissingSentinel()

def _to_json(data: Any):
    return json.loads(data)

async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding='utf-8')
    try:
        if 'application/json' in response.headers['content-type']:
            return json.loads(text)
    except KeyError:
        pass

    return text


def _to_datetime(date: datetime):
    pass


def immuteable(cls):
    original_setattr = cls.__setattr__

    def new_setattr(self, name, value):
        if hasattr(self, name):
            raise AttributeError(f"'{name}' is immuteable and cannot be reassigned.")
        original_setattr(self, name, value)

    cls.__setattr__ = new_setattr
    return cls
