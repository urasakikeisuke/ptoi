try:
    from typing import Iterable, Optional, Tuple
except ImportError:
    from typing_extensions import Iterable, Optional, Tuple


import numpy
from PIL import Image, ImageDraw, ImageFont


def readable_color(color: Iterable) -> Tuple[int, int, int]:
    color = numpy.array(color)
    color_f = color / 255.0
    color = numpy.where(
        color_f <= 0.03928, color_f / 12.92, numpy.power((color_f + 0.055) / 1.055, 2.4)
    )

    Lbg = 0.2126 * color[2] + 0.7152 * color[1] + 0.0722 * color[0]
    Cw = (1.0 + 0.05) / (Lbg + 0.05)
    Cb = (Lbg + 0.05) / (0.0 + 0.05)

    return [0, 0, 0] if Cw < Cb else [255, 255, 255]


class PutTextOnIt:
    def __init__(
        self,
        font_scale: int,
        font_face: str,
    ) -> None:
        """Custom Implement of cv2.putText()
        Args:
            font_scale (int): Font size
            font_face (str): Font path
        """

        self.ttf = ImageFont.truetype(font=font_face, size=font_scale)

    def __call__(
        self,
        img: numpy.ndarray,
        text: str,
        org: Tuple[int, int],
        bgcolor: Tuple[int, int, int],
        color: Optional[Tuple[int, int, int]] = None,
        mode: int = 0
    ) -> numpy.ndarray:
        """Custom Implement of cv2.putText()
        Args:
            img (numpy.ndarray): Source image
            text (str): Display text
            org (Tuple): Text position
            color (Tuple, optional): Font color (Note: BGR) If specified None, use readble color.
            bgcolor (Tuple): Background color (Note: BGR)
            mode (int, optional): Start position. [0: bottomLeft, 1: topLeft, 2: centre] Defaults to 0.
        Returns:
            numpy.ndarray: Return image
        """

        if color is None:
            color = readable_color(bgcolor)

        dummy_draw = ImageDraw.Draw(Image.new("RGB", (0, 0)))
        text_w, text_h = dummy_draw.textsize(text, font=self.ttf)

        text_b = int(0.1 * text_h)
        offset_x = [0, 0, text_w//2]
        offset_y = [text_h, 0, (text_h+text_b)//2]

        x, y = org
        x0 = x - offset_x[mode]
        y0 = y - offset_y[mode]

        img_h, img_w = img.shape[:2]
        if not ((-text_w < x0 < img_w) and (-text_b-text_h < y0 < img_h)):
            raise ValueError(f"Out of bound")

        x1, y1 = max(x0, 0), max(y0, 0)
        x2, y2 = min(x0+text_w, img_w), min(y0+text_h+text_b, img_h)

        text_area = numpy.full(shape=(text_h+text_b, text_w, 3), fill_value=bgcolor, dtype=numpy.uint8)
        text_area[y1-y0:y2-y0, x1-x0:x2-x0] = img[y1:y2, x1:x2]

        img_pil = Image.fromarray(text_area)
        draw = ImageDraw.Draw(img_pil)
        draw.rectangle(xy=[(-10, -text_h), (text_w, y2-y0)], fill=tuple(bgcolor), width=0)
        draw.text(xy=(0, 0), text=text, fill=tuple(color), font=self.ttf)

        text_area = numpy.array(img_pil, dtype=numpy.uint8)
        img[y1:y2, x1:x2] = text_area[y1-y0:y2-y0, x1-x0:x2-x0]

        return img
