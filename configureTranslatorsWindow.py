import os.path
import tkinter as tk
from tkinter import IntVar, StringVar
from windowSelector import WindowSelectorGui

class ConfigureTranslatorsWindowGui(tk.Tk):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        ## Initialize variables
        self.deeplVar = IntVar()
        self.googleVar = IntVar()
        self.libreVar = IntVar()

        ## Initialize gui elements
        self.titleLabel = None
        self.deeplCheckbox = None
        self.googleCheckbox = None
        self.libreCheckbox = None
        self.submitButton = None

        self.set_translator_selector_window_attributes()

    def set_translator_selector_window_attributes(self):
        self.title("Japanese Translator")
        self.geometry("500x250+100+100")
        self.resizable(False, False)

        self.titleLabel = tk.Label(self, text="Please select which translators you want to enable:", font=("Helvetica", 12))
        self.titleLabel.grid(columnspan=3, row=0, pady=(50,0), padx=70)

        self.deeplCheckbox = tk.Checkbutton(self, text="DeepL", font=("Helvetica", 11), variable=self.deeplVar)
        self.deeplCheckbox.grid(column=0, row=1, pady=(40,0), padx=(25,0))

        self.googleCheckbox = tk.Checkbutton(self, text="Google Translate (NMT)", font=("Helvetica", 11), variable=self.googleVar)
        self.googleCheckbox.grid(column=1, row=1, pady=(40,0))

        self.libreCheckbox = tk.Checkbutton(self, text="LibreTranslate", font=("Helvetica", 11), variable=self.libreVar)
        self.libreCheckbox.grid(column=2, row=1, pady=(40,0))

        self.submitButton = tk.Button(self, text="Submit", font=("Helvetica", 11), command=self.submit_translation_selections)
        self.submitButton.grid(columnspan=3, row=2, pady=40, padx=105)

    def submit_translation_selections(self):
        if self.deeplVar.get() or self.googleVar.get():
            self.destroy()
            SetTranslatorAPIWindowGui().run(self.deeplVar.get(), self.googleVar.get(), self.libreVar.get())
        else:
            self.destroy()
            WindowSelectorGui().run()

    def run(self):
        self.mainloop()

class SetTranslatorAPIWindowGui(tk.Tk):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.deeplVar = IntVar()
        self.googleVar = IntVar()
        self.libreVar = IntVar()
        self.deeplAPIVar = StringVar()
        self.googleAPIVar = StringVar()

        ## Initialize gui elements
        self.titleLabel = None
        self.googleLabel = None
        self.deeplLabel = None
        self.submitButton = None
        self.deeplAPIEntry = None
        self.googleAPIEntry = None

        self.set_translator_api_window_attributes()

    def set_translator_api_window_attributes(self):
        self.title("Japanese Translator")
        self.geometry("500x300+100+100")
        self.resizable(False, False)

        self.titleLabel = tk.Label(self, text="Please input your API keys for you selected translators.",
                                   font=("Helvetica", 12))
        self.titleLabel.grid(columnspan=3, row=0, pady=(50, 0), padx=60)

    def set_translator_api_window_input_attributes(self):
        if self.deeplVar:
            self.deeplLabel = tk.Label(self, text="DeepL API key:", font=("Helvetica", 11))
            self.deeplLabel.grid(column=0, row=1, pady=(40,0), padx=(40, 0))

            self.deeplAPIEntry = tk.Entry(self, textvariable=self.deeplAPIVar, font=("Helvetica", 11))
            self.deeplAPIEntry.grid(column=1, row=1, pady=(40, 0))

        if self.googleVar:
            self.googleLabel = tk.Label(self, text="Google API key:", font=("Helvetica", 11))
            self.googleLabel.grid(column=0, row=2, pady=(40, 0), padx=(40, 0))

            self.googleAPIEntry = tk.Entry(self, textvariable=self.googleAPIVar, font=("Helvetica", 11))
            self.googleAPIEntry.grid(column=1, row=2, pady=(40, 0))

        self.submitButton = tk.Button(self, text="Submit", command=self.submit_api_keys, font=("Helvetica", 11))
        self.submitButton.grid(columnspan=3, row=3, pady=40)

    def submit_api_keys(self):

        with open('API_keys.txt', 'r', encoding='utf-8') as file:
            data = file.readlines()

        if not data:
            while len(data) < 3:
                data.append("\n")
        elif len(data) < 3:
            while len(data) < 3:
                data.append("\n")

        data[0] = "keys setup:\n"
        if self.deeplVar:
            data[1]= "deepl: " + self.deeplAPIVar.get() + "\n"
        if self.googleVar:
            data[2] = "google: " + self.googleAPIVar.get() + "\n"

        with open("API_keys.txt", 'w', encoding='utf-8') as file:
            file.writelines(data)

        WindowSelectorGui().run()

    def run(self, deepl_var, google_var, libre_var):
        self.deeplVar = deepl_var
        self.googleVar = google_var
        self.libreVar = libre_var
        self.set_translator_api_window_input_attributes()

        self.mainloop()

if __name__ == "__main__":
    ConfigureTranslatorsWindowGui().run()
