import overlay
import tkinter as tk
from tkinter import ttk, messagebox
import win32gui
import pywinctl

class WindowSelectorGui(tk.Tk):
    def __init__(self, *a, **kw):
        super().__init__(*a, *kw)

        ## Initialize gui elements
        self.label = None
        self.testLabel = None
        self.standaloneButton = None
        self.attachButton = None

        self.set_window_selector_attributes()

    ## Add gui elements
    def set_window_selector_attributes(self):
        self.title("Japanese Translator")
        self.geometry("400x180")
        self.resizable(False, False)

        self.label = tk.Label(self, text="Would you like to attach the translator to a window or \nrun it as a standalone window?", font=("Helvetica", 11))
        self.label.place(x=200, y=50, anchor="center")

        self.standaloneButton = tk.Button(self, text="Run standalone", command=self.submit_standalone_button, font=("Helvetica", 11))
        self.standaloneButton.place(x=100, y=135, anchor="center")

        self.attachButton = tk.Button(self, text="Attach window", command=self.submit_attach_button, font=("Helvetica", 11))
        self.attachButton.place(x=300, y=135, anchor="center")

    ## Run the application standalone on button submission
    def submit_standalone_button(self):
        self.destroy()
        overlay.Overlay().run()

    ## Run the overlay selection gui on button submission
    def submit_attach_button(self):
        self.destroy()
        OverlaySelectorGui().run()

    def run(self):
        self.mainloop()

class OverlaySelectorGui(tk.Tk):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        ## Initialize lists
        self.hwndList = []
        self.winNames = []

        ## Initialize variables
        self.selectedWindowIndex = None

        ## Initialize gui elements
        self.comboBox = None
        self.submitButton = None

        ## Populate lists with hwnd and window names
        win32gui.EnumWindows(self.get_win_enum_handler, None)

        self.set_overlay_selector_window_attributes()

    ##  Handler to add hwnd and windows to lists
    def get_win_enum_handler(self, hwnd, ctx):
        if win32gui.IsWindowVisible( hwnd ) and win32gui.GetWindowText(hwnd) != '':
            self.hwndList.append(hwnd)
            self.winNames.append(win32gui.GetWindowText(hwnd))

    ##  Add gui elements
    def set_overlay_selector_window_attributes(self):
        self.title("Overlay window selector")
        self.geometry("400x600+100+100")
        self.resizable(False, False)
        self.comboBox = ttk.Combobox(self, values=self.winNames)
        self.comboBox.pack(ipadx=100, pady=20)
        self.comboBox.set(self.winNames[0])
        self.submitButton = tk.Button(self, text="Select window", command=self.select_attach_window, font=("Helvetica", 11))
        self.submitButton.pack(pady=40)

    def select_attach_window(self):
        self.selectedWindowIndex = self.comboBox.current()
        if not (pywinctl.getWindowsWithTitle(self.winNames[self.selectedWindowIndex])):
            messagebox.showerror("Error", "Error: Window not found! Please try again.")

        self.destroy()
        overlay.Overlay().run(pywinctl.getWindowsWithTitle(self.winNames[self.selectedWindowIndex])[0], self.hwndList[self.selectedWindowIndex])

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    WindowSelectorGui().run()
