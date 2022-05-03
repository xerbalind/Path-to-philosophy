import bs4
import requests

START = "Science"
STOP = "Philosophy"
BASE_URL = "https://en.wikipedia.org/wiki/"

# Haal de wikipedia pagina op volgens start
response = requests.get(BASE_URL + START)
scraper = bs4.BeautifulSoup(response.text, "html.parser")

# Haal div op met id "bodyContent"
body = scraper.find("div", {"id": "bodyContent"})


def find_link(body):
    # Vind de eerste gewone http link binnen een p tag in de body
    for paragraph in body.find_all("p"):
        s_paragraph = str(paragraph)
        for link in paragraph.find_all("a", href=True):
            if (
                not between_brace(0, s_paragraph.find(str(link)), s_paragraph)
                and ":" not in link["href"]
                and link["href"].startswith("/wiki/")
            ):
                return link["href"]
    return ""


def between_brace(start, stop, paragraph):
    # Tel het aantal open en sluitende accolades tussen start en stop
    open_brace = 0
    close_brace = 0
    for i in paragraph[start:stop]:
        if i == "(":
            open_brace += 1
        elif i == ")":
            close_brace += 1
    return open_brace > close_brace


links = [START]
while links[-1] != STOP:
    response = requests.get(BASE_URL + links[-1])
    scraper = bs4.BeautifulSoup(response.text, "html.parser")
    body = scraper.find("div", {"id": "bodyContent"})
    links.append(find_link(body)[6:])
    print(links[-1])

print(links)
