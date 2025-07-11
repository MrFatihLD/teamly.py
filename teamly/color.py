# color.py

import re
import random
from typing import Tuple


class Color:
    def __init__(self, value: int):
        if not (0 <= value <= 0xFFFFFF):
            raise ValueError("Color value must be between 0x000000 and 0xFFFFFF")
        self.value = value

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"<Color #{self.value:06X}>"

    def to_rgb(self) -> Tuple[int, int, int]:
        r = (self.value >> 16) & 0xFF
        g = (self.value >> 8) & 0xFF
        b = self.value & 0xFF
        return (r, g, b)

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> "Color":
        if not all(0 <= n <= 255 for n in (r, g, b)):
            raise ValueError("RGB values must be between 0 and 255")
        return cls((r << 16) + (g << 8) + b)

    @classmethod
    def from_hex(cls, hex_str: str) -> "Color":
        hex_str = hex_str.strip().lstrip("#")
        if len(hex_str) not in (3, 6):
            raise ValueError("Hex string must be 3 or 6 characters")
        if len(hex_str) == 3:
            hex_str = "".join(c * 2 for c in hex_str)
        return cls(int(hex_str, 16))

    @classmethod
    def from_str(cls, value: str) -> "Color":
        value = value.strip()
        if value.startswith("#"):
            return cls.from_hex(value)
        if value.lower().startswith("rgb"):
            match = re.fullmatch(r"rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)", value)
            if not match:
                raise ValueError("Invalid RGB string format")
            r, g, b = map(int, match.groups())
            return cls.from_rgb(r, g, b)
        raise ValueError(f"Unknown color format: {value}")

    @classmethod
    def red(cls) -> "Color":
        return cls(0xE74C3C)

    @classmethod
    def green(cls) -> "Color":
        return cls(0x2ECC71)

    @classmethod
    def blue(cls) -> "Color":
        return cls(0x3498DB)

    @classmethod
    def yellow(cls) -> "Color":
        return cls(0xF1C40F)

    @classmethod
    def orange(cls) -> "Color":
        return cls(0xE67E22)

    @classmethod
    def purple(cls) -> "Color":
        return cls(0x9B59B6)

    @classmethod
    def teal(cls) -> "Color":
        return cls(0x1ABC9C)

    @classmethod
    def pink(cls) -> "Color":
        return cls(0xFF69B4)

    @classmethod
    def random(cls) -> "Color":
        return cls(random.randint(0x000000, 0xFFFFFF))
