from dataclasses import dataclass, field
from typing import Sequence, Tuple, Optional

import numpy as np
import cv2  # type: ignore

from .font import Font

# Common colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


@dataclass
class InfoBox:
    """A class for drawing info boxes.

    This class is meant to draw an info box, which is comprised of two parts:
    - a **title**, which is a single line of text displayed at the top,
    - a **description**, which consists of multiple lines of text which are
      displayed below the title.

    Each part has its own background, to make them visually distinct.

    Args:
        width: The width (in pixels) of the box.
        title_font: The title font. The font file If not set, the default FiraGO
            font will be used for the title.
        desc_font: The description font. The font file If not set, the default FiraGO
            font will be used for the description.
        title_text_color: The RGB color of the title text.
        desc_text_color: The RGB color of the description.
        title_background: The RGB color of the title background.
        desc_background: The RGB color of the description background.
        font_height_title: The height of the title text.
        font_height_desc: The height of the description text.
        padding: How many pixels to pad the label background on each side.
    """

    width: int
    title_font: Font = field(default_factory=Font.get_default)
    desc_font: Font = field(default_factory=Font.get_default)
    title_text_color: Tuple[int, int, int] = WHITE
    desc_text_color: Tuple[int, int, int] = BLACK
    title_background_color: Tuple[int, int, int] = BLACK
    desc_background_color: Tuple[int, int, int] = WHITE
    font_height_title: int = 25
    font_height_desc: int = 20
    padding: int = 5

    def draw(
        self,
        img: np.ndarray,
        orig_coords: Tuple[int, int],
        desc_lines: Sequence[str],
        title: Optional[str] = None,
    ):
        """Draw the info box.

        Args:
            img: The image to draw on (will not be altered).
            orig_coords: The top-left corner of the info box.
            desc_lines: The lines for the description.
            title: The text for the title. If not present, title
                and its background will not be drawn.
        """

        # Draw title box, if needed
        if title:
            title_orig = (
                orig_coords[0] + self.padding,
                orig_coords[1] + self.font_height_title + self.padding,
            )
            title_box_pt1 = orig_coords
            title_box_pt2 = (
                orig_coords[0] + self.width,  # type: ignore
                orig_coords[1] + self.font_height_title + 2 * self.padding,
            )

            cv2.rectangle(
                img,
                pt1=title_box_pt1,
                pt2=title_box_pt2,
                color=self.title_background_color[::-1],
                thickness=-1,
            )

            self.title_font.font.putText(
                img=img,
                text=title,
                org=title_orig,
                fontHeight=self.font_height_title,
                color=self.title_text_color[::-1],
                thickness=-1,
                line_type=cv2.LINE_AA,
                bottomLeftOrigin=True,
            )

            # Set orig_coords to below title box
            orig_coords = (orig_coords[0], title_box_pt2[1])

        # Draw background
        n_desc = len(desc_lines)

        desc_box_pt1 = orig_coords
        desc_box_pt2 = (
            orig_coords[0] + self.width,
            orig_coords[1]
            + n_desc * self.font_height_desc
            + (n_desc + 1) * self.padding,
        )

        cv2.rectangle(
            img,
            pt1=desc_box_pt1,
            pt2=desc_box_pt2,
            color=self.desc_background_color[::-1],
            thickness=-1,
        )

        # Draw description lines
        for idx, line in enumerate(desc_lines):
            line_orig = (
                orig_coords[0] + self.padding,
                orig_coords[1] + self.padding * (idx + 1) + self.font_height_desc * idx,
            )

            self.desc_font.font.putText(
                img=img,
                text=line,
                org=line_orig,
                fontHeight=self.font_height_desc,
                color=self.desc_text_color[::-1],
                thickness=-1,
                line_type=cv2.LINE_AA,
                bottomLeftOrigin=False,
            )
