# Put Text On It
Let's put text on it

## Install
```bash
pip install ptoi
```

## Usage
```python
import cv2
from ptoi import PutText

# (1) You can specify font_face by path
font_face = "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf"

# (2) Or you can specify font_face by font name
font_face = "Noto Sans Mono"

# (3) Or you can specify font_face by URL
font_face = "https://github.com/notofonts/noto-cjk/raw/main/Sans/Mono/NotoSansMonoCJKjp-Regular.otf"

put_text = PutText(font_face=font_face, font_scale=48)

img = cv2.imread("assets/zidane.jpg")
h, w, _ = img.shape

# If `mode` is specified as 0, the bottom left corner of the text string is placed at the origin.
out_img = put_text(img.copy(), "Mode 0", org=(0, h), bgcolor=(123, 45, 200), mode=0)
cv2.imwrite("assets/zidane.mode.0.jpg", out_img)

# If `mode` is specified as 1, the top left corner of the text string is placed at the origin.
out_img = put_text(img.copy(), "Mode 1", org=(0, 0), bgcolor=(123, 45, 200), mode=1)
cv2.imwrite("assets/zidane.mode.1.jpg", out_img)

# If `mode` is specified as 2, the centre of the text string is placed at the origin.
out_img = put_text(img.copy(), "Mode 2", org=(w//2, h//2), bgcolor=(123, 45, 200), mode=2)
cv2.imwrite("assets/zidane.mode.2.jpg", out_img)
```
