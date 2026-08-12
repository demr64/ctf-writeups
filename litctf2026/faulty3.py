from PIL import Image

img = Image.open("corrupt3.png").convert("RGB")

width, height = img.size

for x in range(width):
    color = img.getpixel((x, 0))
    if(color[0] != 255):
       print(chr(color[0]), end="")


