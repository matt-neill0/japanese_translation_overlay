import pytesseract
import cv2
from PIL import Image
import tkinter as tk
from tkinter import StringVar, filedialog

import windowSelector


class ConfigureTesseractPathGui(tk.Toplevel):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.pathVar = StringVar()

        self.titleLabel = None
        self.pathEntry = None
        self.browseButton = None
        self.submitButton = None
        self.caller = None

        self.set_tesseract_window_attributes()

    def get_current_path(self):
        with open('user_variables.txt', 'r', encoding='utf-8') as file:
            data = file.readlines()

        if len(data) != 4 and len(data) != 3:
            ##  Invalid file, reset user_variables.txt
            data.clear()
            while len(data) < 4:
                data.append("\n")

            with open("user_variables.txt", 'w', encoding='utf-8') as file:
                file.writelines(data)

        else:
            split_data = data[3].split(" ", 1)
            if split_data:
                if split_data[0] == "tesseract_path:":
                    self.pathVar.set(split_data[1])
                else:
                    data[3] = "\n"
            else:
                data[3] = "\n"

    def set_tesseract_window_attributes(self):
        self.get_current_path()
        self.title("Japanese Translator")
        self.geometry("500x250+100+100")
        self.resizable(False, False)

        self.titleLabel = tk.Label(self, text="Please input the path to your tesseract executable:", font=("Helvetica", 12))
        self.titleLabel.grid(column=0, columnspan=2, row=0, pady=(50, 30), padx=70)

        self.pathEntry = tk.Entry(self, textvariable=self.pathVar, width=30, font=("Helvetica", 11))
        self.pathEntry.grid(column=0, row=1, padx=(70,0), sticky="w")

        self.browseButton = tk.Button(self, text="Browse", command=self.on_browse, font=("Helvetica", 11))
        self.browseButton.grid(column=1, row=1, sticky="w")

        self.submitButton = tk.Button(self, text="Submit", command=self.on_submit,font=("Helvetica", 11))
        self.submitButton.grid(columnspan=2, row=2, pady=30)

    def on_browse(self):
        self.pathVar.set(filedialog.askopenfilename(title="Select your tesseract executable"))

    def on_submit(self):
        with open('user_variables.txt', 'r', encoding='utf-8') as file:
            data = file.readlines()

        if len(data) != 4 and len(data) != 3:
            ##  Invalid file, reset user_variables.txt
            data.clear()
            while len(data) < 4:
                data.append("\n")

            with open("user_variables.txt", 'w', encoding='utf-8') as file:
                file.writelines(data)

        elif len(data) == 3:
            data.append("\n")
            with open("user_variables.txt", 'w', encoding='utf-8') as file:
                file.writelines(data)

        data[3] = "tesseract_path: " + self.pathVar.get()
        with open("user_variables.txt", 'w', encoding='utf-8') as file:
            file.writelines(data)

        if self.caller == "FTS":
            self.destroy()
            windowSelector.WindowSelectorGui().run()
        else:
            self.destroy()


    def run(self, caller = None):
        self.caller = caller
        if caller == "FTS":
            self.master.withdraw()
        self.mainloop()


def frame_ocr(image_path):
    img = Image.open(image_path)

    text = pytesseract.image_to_string(img, lang='jpn')
    print(text)