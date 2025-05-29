from pynput import mouse
from PIL import ImageGrab

def get_pixel_color(x, y):
    image = ImageGrab.grab(bbox=(x, y, x+1, y+1))  
    pixel = image.getpixel((0, 0))
    return pixel

def on_click(x, y, button, pressed):
    if pressed:
        rgb = get_pixel_color(x, y)
        print(f"Pressed Coordinates: ({x}, {y}) - RGB: {rgb}")
        return False  

print("Press For Get RGB Values...")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
