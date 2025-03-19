import mss
from pynput.mouse import Listener
import tkinter as tk
import overlay

class MyException(Exception):
    pass

click_and_drag_overlay = None
root = None

def start_overlay():
    global click_and_drag_overlay, root
    root = tk.Tk()
    root.withdraw()
    click_and_drag_overlay = tk.Toplevel(root)
    click_and_drag_overlay.overrideredirect(True)
    click_and_drag_overlay.attributes("-alpha", 0.3)
    click_and_drag_overlay.lift()

def update_overlay(x_1, y_1, x_2, y_2):
    if click_and_drag_overlay:
        click_and_drag_overlay.geometry(f"{abs(x_2-x_1)}x{abs(y_2-y_1)}+{min(x_1, x_2)}+{min(y_1, y_2)}")
        click_and_drag_overlay.config(bg="blue")
        click_and_drag_overlay.update_idletasks()

def hide_overlay():
    if click_and_drag_overlay:
        click_and_drag_overlay.destroy()

def grab(x, y, w, h):
    print(f"Capturing region: x={x}, y={y}, width={w}, height={h}")

    with mss.mss() as sct:
        region = {"left": x, "top": y, "width": w, "height": h}
        sct_img = sct.grab(region)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output="grab.png")
    overlay.Overlay().capture_complete()


click1 = 0
x1 = 0
y1 = 0

def on_click(x, y, button, pressed):
    global click1, x1, y1, listener
    if pressed:
        if click1 == 0:
            x1 = x
            y1 = y
            click1 = 1
            start_overlay()
    elif not pressed and click1 == 1:
        hide_overlay()

        width = abs(x - x1)
        height = abs(y - y1)
        x_min = min(x, x1)
        y_min = min(y, y1)

        grab(x_min, y_min, width, height)
        listener.stop()
        click1 = 0

def on_move(x, y):
    if click1:
        update_overlay(x1, y1, x, y)

def start():
    global listener
    listener = Listener(on_move, on_click, None)

    try:
        listener.start()
    except MyException as e:
        print(f'{e.args[0]} was clicked')
