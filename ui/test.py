from PIL import ImageGrab


x = 100
y = 200

image = ImageGrab.grab(bbox=(x, y, x+1, y+1))
t = image.getpixel((x, y))
print(t)
