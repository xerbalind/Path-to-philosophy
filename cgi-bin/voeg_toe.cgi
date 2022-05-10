#!/usr/bin/env python3
import json
import cgi
import bs4
import requests


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
    # als het aantal open accolades groter is dan  het aantal sluitende accolades, zit de link tussen de accolades
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


# Lees data verstuurd door JavaScript
parameters = cgi.FieldStorage()

begin = parameters.getvalue("start")
eind = parameters.getvalue("end")
language = parameters.getvalue("language")

# Bereken te verzenden data
path = get_path(language, begin, eind)

if type(path) == str:
    body = {"error": path}
else:
    body = {"path": path}

# Stuur antwoord terug
print("Content-Type: application/json")
print()  # Lege lijn na headers
print(json.dumps(body))
