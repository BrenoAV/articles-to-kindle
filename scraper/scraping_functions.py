from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_article_text_from_url_bbc_future(url: str) -> str:
    with urlopen(url) as response:
        content = response.read()
    soup = BeautifulSoup(content, "html.parser")
    # Getting the text with the news
    article_title: str = soup.find(
        "h1",
        attrs={"class": "article-headline__text b-reith-sans-font b-font-weight-300"},
    ).text
    author_name: str = soup.find(
        "a", attrs={"class": "author-unit__text b-font-family-serif"}
    ).text
    date_time: str = soup.find(
        "span", attrs={"class": "b-font-family-serif b-font-weight-300"}
    ).text
    body_content_intro: str = soup.find(
        name="div", attrs={"class": "article__intro b-font-family-serif"}
    ).text
    body_content: str = soup.find(
        name="div", attrs={"class": "article__body-content"}
    ).text
    body_content: str = body_content.replace(
        body_content_intro, body_content_intro + " -> "
    )
    # exclude social medias below of the text
    body_content: str = body_content[: body_content.find("--")]
    return article_title, author_name, date_time, body_content
