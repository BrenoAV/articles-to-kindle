import os
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

from scraper.scraping_functions import get_article_text_from_url_bbc_future
from utils.email_tools import gmail_authenticate, send_article
from utils.helper_functions import convert_text_to_epub_bbc_future


class MyApp(tk.Tk):
    def __init__(self, OUR_EMAIL: str, KINDLE_EMAIL: str):
        super().__init__()

        self.OUR_EMAIL = OUR_EMAIL
        self.KINDLE_EMAIL = KINDLE_EMAIL

        self.title("Articles to Kindle")
        self.geometry("420x120")

        self.title_font = Font(family="verdana", size=20)
        self.common_font = Font(family="verdana", size=14)
        self.url_variable = tk.StringVar(self)

        self.container = ttk.Frame(self)
        self.container.pack()

        self.label = ttk.Label(
            self.container, text="Articles to Kindle", font=self.title_font
        )
        self.label.pack()

        self.container_entry = ttk.Frame(self)
        self.container_entry.pack()

        self.label_url = ttk.Label(
            self.container_entry, text="URL", font=self.common_font
        )
        self.label_url.pack(side=tk.LEFT, padx=6)

        self.entry_link = ttk.Entry(
            self.container_entry,
            width=45,
            textvariable=self.url_variable,
        )
        self.entry_link.pack(side=tk.RIGHT)

        self.container_buttons = ttk.Frame(self)
        self.container_buttons.pack()
        self.button_clean = ttk.Button(
            self.container_buttons, text="Clean Entry", command=self.clean_entry_clicked
        )
        self.button_clean.pack(side=tk.LEFT, padx=10, pady=10)
        self.button_send = ttk.Button(
            self.container_buttons,
            text="Send article to Kindle",
            command=self.send_artcile_clicked,
        )
        self.button_send.pack(side=tk.LEFT)

    def clean_entry_clicked(self):
        self.url_variable.set("")

    def send_artcile_clicked(self):
        url = self.url_variable.get().strip().lower()
        article_title, author_name, date, body_content = get_article_text_from_url_bbc_future(
            url
        )
        output_filepath = "outputs/"
        epub_file = os.path.join(output_filepath, f"{article_title}.epub")
        convert_text_to_epub_bbc_future(
            body_content, article_title, author_name, date, output_filepath
        )

        service = gmail_authenticate()  # you need to have credentials.json

        send_article(
            service,
            self.OUR_EMAIL,
            self.KINDLE_EMAIL,
            article_title,
            "news",
            article_filename=epub_file,
        )


