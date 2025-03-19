from windowSelector import WindowSelectorGui
from configureTranslatorsWindow import ConfigureTranslatorsWindowGui
import os.path


if __name__ == "__main__":
    if not os.path.isfile("user_variables.txt"):
        open("user_variables.txt", "w")
        ConfigureTranslatorsWindowGui().run()

    with open('user_variables.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()

    if not data:
        ConfigureTranslatorsWindowGui().run()

    elif data[0] != "keys setup:\n":
        ConfigureTranslatorsWindowGui().run()

    WindowSelectorGui().run()
