import bs4
import requests

START = "Python (programming language)"
STOP = "Psychology"


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


def get_path(language, begin, eind):
    # Haal de paden op tussen start en stop
    current_link = "/wiki/" + begin
    path = []
    base_url = f"https://{language}.wikipedia.org"
    while len(path) == 0 or path[-1] != eind:
        response = requests.get(base_url + current_link)
        scraper = bs4.BeautifulSoup(response.text, "html.parser")

        title = scraper.find("h1", {"id": "firstHeading"}).text
        if title in path:
            return "Cycle detected at " + title
        path.append(title)

        body = scraper.find("div", {"id": "bodyContent"})
        current_link = find_link(body)
        if not current_link:
            return "No link found in page " + title
    return path


print(get_path("en", START, STOP))
