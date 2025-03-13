import tkinter as tk
import win32gui
from tkinter import messagebox
from pynput import keyboard, mouse

class MyException(Exception):
    pass

## Custom mapping for more conventional button names
BUTTON_NAMES = {
    mouse.Button.left: "Left Click",
    mouse.Button.right: "Right Click",
    mouse.Button.middle: "Middle Click",
    mouse.Button.x1: "Mouse4",
    mouse.Button.x2: "Mouse5",
}

class Overlay(tk.Tk):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        ## Initialize variables
        self.chosenWindow = None
        self.chosenHwnd = None
        self.clickAndDragHotkey = mouse.Button.x2
        self.mouseBindListener = None
        self.keyboardBindListener = None

        ## Initialize gui elements
        self.mainFrame = None
        self.secondaryFrame = None
        self.canvas = None
        self.scrollbar = None
        self.settingsLabel = None
        self.currentBindLabel = None
        self.bindButton = None
        self.bindLabel = None

        self.set_window_attributes()

    ## Add gui elements
    def set_window_attributes(self):
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.title("Japanese Translation Overlay")
        self.geometry("400x400+100+100")

        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill="both", expand=1)

        self.canvas = tk.Canvas(self.mainFrame)
        self.canvas.pack(side="left", fill="both", expand=1)

        self.scrollbar = tk.Scrollbar(self.mainFrame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.secondaryFrame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.secondaryFrame, anchor="nw")

        self.settingsLabel = tk.Label(self.secondaryFrame, text="Settings", font=("Helvetica", 14))
        self.settingsLabel.grid(row=3, column=0, padx=(20,0), pady=(10, 0), sticky="w")

        self.bindButton = tk.Button(self.secondaryFrame, text="Rebind key", command=self.bind_click_and_drag_hotkey, font=("Helvetica", 11))
        self.bindButton.grid(row=4, column=0, padx=(20,60), pady=(10, 0))

        self.currentBindLabel = tk.Label(self.secondaryFrame, text="Bound key:", font=("Helvetica", 11))
        self.currentBindLabel.grid(row=4, column=1, padx=(0,20), pady=(10, 0))

        self.bindLabel = tk.Label(self.secondaryFrame, text="Mouse5", font=("Helvetica", 11))
        self.bindLabel.grid(row=4, column=2, padx=(0, 0), pady=(10, 0))

    def update_overlay(self):
        if win32gui.IsWindow(self.chosenHwnd):
            x, y, w, h = self.chosenWindow.left, self.chosenWindow.top, self.chosenWindow.width, self.chosenWindow.height
            self.geometry(f"400x{h-10}+{x+w}+{y+1}")
            self.after(10, self.update_overlay)
        else:
            self.destroy()

    def on_mouse_bind_click(self, x, y, button, pressed):
        print(pressed)
        if not pressed:
            self.clickAndDragHotkey = button
            self.bindLabel.config(text=str(BUTTON_NAMES.get(button, str(button))))
            self.mouseBindListener.stop()
            self.keyboardBindListener.stop()

    def on_keyboard_bind_click(self, key):
        try:
            if key == keyboard.Key.esc:
                self.keyboardBindListener.stop()
            else:
                self.clickAndDragHotkey = key
                self.bindLabel.config(text=key)
                self.keyboardBindListener.stop()
                self.mouseBindListener.stop()
        except AttributeError:
            messagebox.showerror("Special key exception", "Attempted to bind special key!\nPlease bind the hotkey to a standard button.")


    def bind_click_and_drag_hotkey(self):
        self.mouseBindListener = mouse.Listener(None, self.on_mouse_bind_click, None)
        self.keyboardBindListener = keyboard.Listener(self.on_keyboard_bind_click, None)
        try:
            self.mouseBindListener.start()
            self.keyboardBindListener.start()
        except MyException as e:
            print(f'{e.args[0]} was clicked')

    def run(self, chosen_window = None, chosen_hwnd = None):
        self.chosenHwnd = chosen_hwnd
        self.chosenWindow = chosen_window
        if chosen_window is not None and chosen_hwnd is not None:
            self.update_overlay()
        self.mainloop()