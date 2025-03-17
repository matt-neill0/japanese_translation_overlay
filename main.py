from windowSelector import WindowSelectorGui
from configureTranslatorsWindow import ConfigureTranslatorsWindowGui
import os.path


if __name__ == "__main__":
    if not os.path.isfile("API_keys.txt"):
        open("API_keys.txt", "w")
        ConfigureTranslatorsWindowGui().run()

    with open('API_keys.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()

    if not data:
        ConfigureTranslatorsWindowGui().run()

    elif data[0] != "keys setup:\n":
        ConfigureTranslatorsWindowGui().run()

    WindowSelectorGui().run()
