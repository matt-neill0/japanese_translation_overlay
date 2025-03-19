import tkinter as tk
from tkinter import IntVar, StringVar

import translateText

class ConfigureTranslatorsWindowGui(tk.Toplevel):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        ## Initialize variables
        self.deeplVar = IntVar()
        self.googleVar = IntVar(value=0)
        self.libreVar = IntVar()
        self.caller = None

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
            SetTranslatorAPIWindowGui().run(self.deeplVar.get(), self.googleVar.get(), self.caller)
        else:
            self.destroy()
            if self.caller == "FTS":
                translateText.ConfigureTesseractPathGui().run(self.caller)
            else:
                self.destroy()

    def run(self, caller = None):
        self.caller = caller
        if caller == "FTS":
            self.master.withdraw()
        self.mainloop()

class SetTranslatorAPIWindowGui(tk.Tk):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.deeplVar = IntVar()
        self.googleVar = IntVar()
        self.deeplAPIVar = StringVar()
        self.googleAPIVar = StringVar()
        self.caller = None

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

    def get_current_keys(self):
        with open('user_variables.txt', 'r', encoding='utf-8') as file:
            data = file.readlines()

        def split_line(line):
            return line.split()

        if len(data) != 4 and len(data) != 3:
            ##  Invalid file, reset user_variables.txt
            data.clear()
            while len(data) < 4:
                data.append("\n")

            with open("user_variables.txt", 'w', encoding='utf-8') as file:
                file.writelines(data)

        else:
            for i in range(1,3):
                split_data = split_line(data[i])
                if split_data:
                    if i == 1 and split_data[0] == "deepl:":
                        self.deeplAPIVar.set(split_data[1])
                    elif i == 2 and split_data[0] == "google:":
                        self.googleAPIVar.set(split_data[1])
                    else:
                        ##  Invalid entry, reset line
                        data[i] = "\n"
                else:
                    ##  Invalid entry, reset line
                    data[i] = "\n"

    def set_translator_api_window_input_attributes(self):
        self.get_current_keys()
        if self.deeplVar:
            self.deeplLabel = tk.Label(self, text="DeepL API key:", font=("Helvetica", 11))
            self.deeplLabel.grid(column=0, row=1, pady=(40,0), padx=(40, 0))

            self.deeplAPIEntry = tk.Entry(self, textvariable=self.deeplAPIVar, font=("Helvetica", 11))
            self.deeplAPIEntry.insert(0, self.deeplAPIVar.get())
            self.deeplAPIEntry.grid(column=1, row=1, pady=(40, 0))

        if self.googleVar:
            self.googleLabel = tk.Label(self, text="Google API key:", font=("Helvetica", 11))
            self.googleLabel.grid(column=0, row=2, pady=(40, 0), padx=(40, 0))

            self.googleAPIEntry = tk.Entry(self, textvariable=self.googleAPIVar, font=("Helvetica", 11))
            self.googleAPIEntry.insert(0, self.googleAPIVar.get())
            self.googleAPIEntry.grid(column=1, row=2, pady=(40, 0))

        self.submitButton = tk.Button(self, text="Submit", command=self.submit_api_keys, font=("Helvetica", 11))
        self.submitButton.grid(columnspan=3, row=3, pady=40)

    def submit_api_keys(self):
        with open('user_variables.txt', 'r', encoding='utf-8') as file:
            data = file.readlines()

        if not data:
            while len(data) < 3:
                data.append("\n")
        elif len(data) < 3:
            while len(data) < 3:
                data.append("\n")

        data[0] = "keys setup:\n"
        if self.deeplVar:
            data[1]= "deepl: " + self.deeplAPIEntry.get() + "\n"
        if self.googleVar:
            data[2] = "google: " + self.googleAPIEntry.get() + "\n"

        with open("user_variables.txt", 'w', encoding='utf-8') as file:
            file.writelines(data)

        if self.caller == "FTS":
            self.destroy()
            translateText.ConfigureTesseractPathGui().run("FTS")
        else:
            self.destroy()

    def run(self, deepl_var = None, google_var = None, caller = None):
        self.deeplVar = deepl_var
        self.googleVar = google_var
        self.caller = caller
        self.set_translator_api_window_input_attributes()

        self.mainloop()