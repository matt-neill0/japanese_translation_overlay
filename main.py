from windowSelector import WindowSelectorGui
from configureTranslatorsWindow import ConfigureTranslatorsWindowGui
from dotenv import load_dotenv, set_key, get_key
import os

def configure():
    load_dotenv()

def set_env_variable(key, value, env_file=".env"):
    load_dotenv(env_file)
    os.environ[key] = value
    set_key(env_file, key, value)

if __name__ == "__main__":
    configure()
    if get_key(".env", "FIRST_TIME_SETUP") == "1":
        WindowSelectorGui().run()
    else:
        ConfigureTranslatorsWindowGui().run()
