from pathlib import Path
import tempfile

try:
    from typing import Iterable, Optional, Tuple
except ImportError:
    from typing_extensions import Iterable, Optional, Tuple

from typing import Dict
from urllib.parse import urlparse

import numpy
import wget
from matplotlib import font_manager
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


class FontManager:
    def __init__(self) -> None:
        self.name_to_path: Dict[str, str] = {}
        self.path_to_name: Dict[str, str] = {}

        for path in font_manager.findSystemFonts():
            try:
                name = ImageFont.FreeTypeFont(path).getname()[0]
            except:
                continue

            self.name_to_path[name] = path
            self.path_to_name[path] = name

    def download_font(self, font_url: str, font_path: Optional[str] = None) -> str:
        """Download font from URL.

        Args:
            font_url (str): Font URL.
            font_path (Optional[str], optional): Font path. If not specified, will be download in tmp directory. Defaults to None.

        Returns:
            str: Font path.
        """

        if font_path is None:
            font_path = tempfile.mkdtemp()

        dst_path = wget.download(font_url, out=font_path)
        name = ImageFont.FreeTypeFont(dst_path).getname()[0]

        self.name_to_path[name] = dst_path
        self.path_to_name[dst_path] = name

        return dst_path

    def get_font_path(self, font_name: str) -> Optional[str]:
        """Get font path from font name.

        Args:
            font_name (str): Font name.

        Returns:
            Optional[str]: Font path. If not found, return None.
        """

        if font_name in self.name_to_path:
            return self.name_to_path[font_name]

        return None

    def get_font_name(self, font_path: str) -> Optional[str]:
        """Get font name from font path.

        Args:
            font_path (str): Font path.

        Returns:
            Optional[str]: Font name. If not found, return None.
        """

        if font_path in self.path_to_name:
            return self.path_to_name[font_path]

        return None


class PutText:
    def __init__(
        self,
        font_scale: int,
        font_face: str,
    ) -> None:
        """Custom Implement of cv2.putText()
        Args:
            font_scale (int): Font size
            font_face (str): Font family name path to the installed font or URL of the font.
        """

        fm = FontManager()

        if urlparse(font_face).scheme in ("http", "https"):
            font_face = fm.download_font(font_face)
        elif Path(font_face).exists():
            font_face = str(Path(font_face).absolute().resolve())
        elif font_face in fm.name_to_path:
            font_face = fm.name_to_path[font_face]
        else:
            raise ValueError(f"Invalid font_face: {font_face}")

        if not Path(font_face).exists():
            raise ValueError(f"Invalid font_face: {font_face}")

        self.ttf = ImageFont.truetype(font=font_face, size=font_scale)

    def __call__(
        self,
        img: numpy.ndarray,
        text: str,
        org: Tuple[int, int],
        bgcolor: Tuple[int, int, int],
        color: Optional[Tuple[int, int, int]] = None,
        mode: int = 0,
    ) -> numpy.ndarray:
        """Custom Implement of cv2.putText()
        Args:
            img (numpy.ndarray): Source image
            text (str): Display text
            org (Tuple): Text position (x, y)
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
        offset_x = [0, 0, text_w // 2]
        offset_y = [text_h, 0, (text_h + text_b) // 2]

        x, y = org
        x0 = x - offset_x[mode]
        y0 = y - offset_y[mode]

        img_h, img_w = img.shape[:2]
        x1, y1 = max(x0, 0), max(y0, 0)
        x2, y2 = min(x0 + text_w, img_w), min(y0 + text_h + text_b, img_h)

        text_area = numpy.full(
            shape=(text_h + text_b, text_w, 3), fill_value=bgcolor, dtype=numpy.uint8
        )
        text_area[y1 - y0 : y2 - y0, x1 - x0 : x2 - x0] = img[y1:y2, x1:x2]

        img_pil = Image.fromarray(text_area)
        draw = ImageDraw.Draw(img_pil)
        draw.rectangle(
            xy=[(-10, -text_h), (text_w, y2 - y0)], fill=tuple(bgcolor), width=0
        )
        draw.text(xy=(0, 0), text=text, fill=tuple(color), font=self.ttf)

        text_area = numpy.array(img_pil, dtype=numpy.uint8)
        img[y1:y2, x1:x2] = text_area[y1 - y0 : y2 - y0, x1 - x0 : x2 - x0]

        return img
