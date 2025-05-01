import pyautogui
from pynput import mouse
from PIL import ImageGrab

def get_pixel_color(x, y):
    image = ImageGrab.grab(bbox=(x, y, x+1, y+1))  # Sadece 1x1 alan al
    pixel = image.getpixel((0, 0))
    return pixel

def on_click(x, y, button, pressed):
    if pressed:
        rgb = get_pixel_color(x, y)
        print(f"Tıklanan Koordinat: ({x}, {y}) - RGB: {rgb}")
        return False  # Tek bir tıklamadan sonra dinlemeyi bitir

print("RGB değeri almak için bir noktaya tıklayın...")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
