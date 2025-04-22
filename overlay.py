import tkinter as tk
import win32gui
from tkinter import messagebox
from pynput import keyboard, mouse
from snippingTool import snip_once

import configureTranslatorsWindow
import translateText


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
        self.bindTitleLabel = None
        self.bindButton = None
        self.bindLabel = None
        self.APIKeysLabel = None
        self.APIKeysButton = None
        self.tesseractLabel = None
        self.tesseractButton = None

        self.set_window_attributes()

    ## Add gui elements
    def set_window_attributes(self):
        self.resizable(False, False)
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

        ##  Row 4 - Settings title line
        self.settingsLabel = tk.Label(self.secondaryFrame, text="Settings", font=("Helvetica", 14))
        self.settingsLabel.grid(row=4, column=0, padx=(20,0), pady=(10, 0), sticky="w")

        ##  Row 5 - Configure bound key line
        self.bindTitleLabel = tk.Label(self.secondaryFrame, text="Rebind click and drag hotkey:", font=("Helvetica", 12))
        self.bindTitleLabel.grid(row=5, column=0, padx=(20,0), pady=(10,0), sticky="w")
        self.bindButton = tk.Button(self.secondaryFrame, text="Rebind key", command=self.bind_click_and_drag_hotkey, font=("Helvetica", 11))
        self.bindButton.grid(row=5, column=1, padx=(20,0), pady=(10, 0))

        ##  Row 6 - Bound key line
        self.currentBindLabel = tk.Label(self.secondaryFrame, text="Currently bound key:", font=("Helvetica", 11))
        self.currentBindLabel.grid(row=6, column=0, padx=(20,0), pady=(10, 0), sticky='w')
        self.bindLabel = tk.Label(self.secondaryFrame, text="Mouse5", font=("Helvetica", 11))
        self.bindLabel.grid(row=6, column=1, padx=(20, 0), pady=(10, 0))

        ##  Row 7 - Configure API Key line
        self.APIKeysLabel = tk.Label(self.secondaryFrame, text="Configure API keys:", font=("Helvetica", 12))
        self.APIKeysLabel.grid(row=7, column=0, padx=(20,60), pady=(20,0), sticky="w")
        self.APIKeysButton = tk.Button(self.secondaryFrame, text="Configure", command=self.configure_API_keys, font=("Helvetica", 11))
        self.APIKeysButton.grid(row=7, column=1, padx=(20,0), pady=(20,0))

        ##  Row 8 - Configure tesseract path line
        self.tesseractLabel = tk.Label(self.secondaryFrame, text="Configure tesseract path:", font=("Helvetica", 12))
        self.tesseractLabel.grid(row=8, column=0, padx=(20,60), pady=(20,0), stick="w")
        self.tesseractButton = tk.Button(self.secondaryFrame, text="Configure", command=self.configure_tesseract, font=("Helvetica", 11))
        self.tesseractButton.grid(row=8, column=1, padx=(20,0), pady=(20,0))

    def configure_API_keys(self):
        configureTranslatorsWindow.ConfigureTranslatorsWindowGui().run("overlay")

    def configure_tesseract(self):
        translateText.ConfigureTesseractPathGui().run()

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
        self.mouseBindListener.stop()
        self.keyboardBindListener.stop()
        self.mouseBindListener = mouse.Listener(None, self.on_mouse_bind_click, None)
        self.keyboardBindListener = keyboard.Listener(self.on_keyboard_bind_click, None)
        try:
            self.mouseBindListener.start()
            self.keyboardBindListener.start()
        except MyException as e:
            print(f'{e.args[0]} was clicked')

    def hotkey_mouse_listen(self, x, y, button, pressed):
        try:
            if button == self.clickAndDragHotkey and not pressed:
                self.after(0, self.do_snip)
        except AttributeError:
            messagebox.showerror("Special key exception")

    def hotkey_keyboard_listen(self, key):
        try:
            if key == self.clickAndDragHotkey:
                self.after(0, self.do_snip)
        except AttributeError:
            messagebox.showerror("Special key exception")

    def hotkey_listen(self):
        self.mouseBindListener = mouse.Listener(None, self.hotkey_mouse_listen, None)
        self.keyboardBindListener = keyboard.Listener(self.hotkey_keyboard_listen, None)
        try:
            self.mouseBindListener.start()
            self.keyboardBindListener.start()
        except MyException as e:
            print(f'{e.args[0]} was clicked')

    def do_snip(self):
        img = snip_once("snip.png")

    def run(self, chosen_window = None, chosen_hwnd = None):
        self.chosenHwnd = chosen_hwnd
        self.chosenWindow = chosen_window
        if chosen_window is not None and chosen_hwnd is not None:
            self.update_overlay()
        self.hotkey_listen()
        self.mainloop()

if __name__ == "__main__":
    Overlay().run()