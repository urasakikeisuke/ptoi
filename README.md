# Put Text On It
Let's put text on it

## Install
```bash
pip install ptoi
```

## Usage
```python3
import cv2
from ptoi import PutTextOnIt

font = "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf"
put_text = PutTextOnIt(font_face=font, font_scale=32)

img = put_text(cv2.imread("assets/zidane.jpg"), "Hello World", org=(100, 100), bgcolor=(123, 45, 200))
cv2.imwrite("assets/zidane.out.jpg", img)
```

## Example
![original](assets/zidane.jpg)

![text](assets/zidane.out.jpg)
