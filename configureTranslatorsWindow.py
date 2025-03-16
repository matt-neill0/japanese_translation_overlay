import tkinter as tk
from tkinter import IntVar
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
        self.geometry("500x300+100+100")
        self.resizable(False, False)

        self.titleLabel = tk.Label(self, text="Please select which translators you want to enable:", font=("Helvetica", 12))
        self.titleLabel.grid(columnspan=3, row=0, pady=(50,0), padx=70)

        self.deeplCheckbox = tk.Checkbutton(self, text="DeepL", font=("Helvetica", 11), variable=self.deeplVar)
        self.deeplCheckbox.grid(column=0, row=1, pady=(20,0), padx=(25,0))

        self.googleCheckbox = tk.Checkbutton(self, text="Google Translate (NMT)", font=("Helvetica", 11), variable=self.googleVar)
        self.googleCheckbox.grid(column=1, row=1, pady=(20,0))

        self.libreCheckbox = tk.Checkbutton(self, text="LibreTranslate", font=("Helvetica", 11), variable=self.libreVar)
        self.libreCheckbox.grid(column=2, row=1, pady=(20,0))

        self.submitButton = tk.Button(self, text="Submit", font=("Helvetica", 11), command=self.submit_translation_selections)
        self.submitButton.grid(columnspan=3, row=2, pady=20, padx=105)

    def submit_translation_selections(self):
        if self.deeplVar.get() or self.googleVar.get():
            SetTranslatorAPIWindowGui().run()
        else:
            self.destroy()
            WindowSelectorGui().run()

    def run(self):
        self.mainloop()

class SetTranslatorAPIWindowGui(tk.Tk):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        ## Initialize gui elements
        self.titleLabel = None

        self.set_translator_api_window_attributes()

    def set_translator_api_window_attributes(self):
        self.title("Japanese Translator")
        self.geometry("500x300+100+100")
        self.resizable(False, False)

        self.titleLabel = tk.Label(self, text="Please select which translators you want to enable:",
                                   font=("Helvetica", 12))
        self.titleLabel.grid(columnspan=3, row=0, pady=(50, 0), padx=70)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    ConfigureTranslatorsWindowGui().run()
