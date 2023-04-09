import os
import sys

from dotenv import load_dotenv

from gui.app import MyApp

load_dotenv()
OUR_EMAIL = os.getenv("OUR_EMAIL")
KINDLE_EMAIL = os.getenv("KINDLE_EMAIL")


if __name__ == "__main__":
    app = MyApp(OUR_EMAIL, KINDLE_EMAIL)
    app.mainloop()

    sys.exit()
