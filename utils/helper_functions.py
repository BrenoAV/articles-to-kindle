import os
import yaml
import pypandoc
from pathlib import Path


class Metadata:
    def __init__(self, title: str, author: str, publisher: str, date: str):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.date = date

    def create_metadata_yaml(self, output_path: Path):
        with open(
            os.path.join(output_path, f"{self.title}.yaml"), "w", encoding="utf-8"
        ) as meta_file:
            yaml.dump(
                {
                    "title": [{"type": "main", "text": self.title}],
                    "creator": [{"role": "author", "text": self.author}],
                    "publisher": self.publisher,
                    "date": self.date,
                },
                meta_file,
            )


def convert_text_to_epub_bbc_future(
    string_content, title: str, author: str, date: str, output_filepath
):
    publisher = "BBC Future"
    output_path = Path(output_filepath)
    output_path.mkdir(parents=True, exist_ok=True)
    metadata = Metadata(title, author, publisher, date)
    metadata.create_metadata_yaml(output_path)
    return pypandoc.convert_text(
        string_content,
        "epub",
        format="md",
        outputfile=os.path.join(output_path, f"{title}.epub"),
        extra_args=["--metadata-file", os.path.join(output_path, f"{title}.yaml")],
    )
