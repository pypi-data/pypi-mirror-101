from pathlib import Path
from typing import Any, Union

import cv2  # type: ignore


class Font:
    """A class for loading FreeType fonts for use with OpenCV.

    Attributes:
        font: The cv2 FreeType font, which enables drawing text on images with
            ``putText`` and getting the size of the  text with ``getTextSize``.
    """

    _default_font: Any
    font: Any

    @classmethod
    def get_default(cls) -> Any:
        """ Get the default FiraGo-Regular font. """

        if not getattr(cls, "_default_font", None):
            default_font_file = Path(__file__).parent / "fonts/FiraGO-Regular.ttf"
            cls._default_font = cls(default_font_file)

        return cls._default_font

    def __init__(self, font_file_name: Union[str, Path]):
        self.font = cv2.freetype.createFreeType2()
        self.font.loadFontData(fontFileName=str(font_file_name), id=0)
