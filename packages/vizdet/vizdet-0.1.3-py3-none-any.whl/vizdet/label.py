from dataclasses import dataclass, field
from typing import Tuple, Optional

import numpy as np
import cv2  # type: ignore

from .font import Font

# Common colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


@dataclass
class Label:
    """A class for drawing free-standing text labels.

    Args:
        font: The font for the label. If not set, the default FiraGO font will be used.
        text_color: The RGB color for the text.
        background_color: The RGB color for the background. If set to ``None``, no
            background will be drawn.
        font_height: Height of the text of the label.
        padding: How many pixels to pad the text on all sides for the background.
    """

    font: Font = field(default_factory=Font.get_default)
    text_color: Tuple[int, int, int] = BLACK
    background_color: Optional[Tuple[int, int, int]] = WHITE
    font_height: int = 25
    padding: int = 5

    def draw(
        self,
        img: np.ndarray,
        center_coords: Tuple[int, int],
        text: str,
    ):
        """Draw the label on the image.

        Args:
            img: The image to draw on
            center_coords: The center of the label
            text: The text (label) to draw
        """

        # Prepare coordinates
        bsize = self.font.font.getTextSize(text, self.font_height, -1)
        text_orig = (
            center_coords[0] - bsize[0][0] // 2,
            center_coords[1] + bsize[0][1] // 2,
        )

        box_pt1 = (text_orig[0] - self.padding, text_orig[1] + bsize[1] + self.padding)
        box_pt2 = (
            text_orig[0] + bsize[0][0] + self.padding,
            text_orig[1] - bsize[0][1] - self.padding,
        )

        # Draw text and bounding box
        if self.background_color:
            cv2.rectangle(
                img,
                pt1=box_pt1,
                pt2=box_pt2,
                color=self.background_color[::-1],
                thickness=-1,
            )

        self.font.font.putText(
            img=img,
            text=text,
            org=text_orig,
            fontHeight=self.font_height,
            color=self.text_color[::-1],
            thickness=-1,
            line_type=cv2.LINE_AA,
            bottomLeftOrigin=True,
        )
