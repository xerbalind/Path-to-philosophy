#!/usr/bin/env python3
import json
import cgi
import bs4
import requests

# START = "Ghent_University"
# STOP = "Philosophy"
BASE_URL = "https://en.wikipedia.org/wiki/"
#
# # Haal de wikipedia pagina op volgens start
# response = requests.get(BASE_URL + START)
# scraper = bs4.BeautifulSoup(response.text, "html.parser")
#
# # Haal div op met id "bodyContent"
# body = scraper.find("div", {"id": "bodyContent"})


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


def get_path(begin, eind):
    # Haal de paden op tussen start en stop
    path = [begin]
    while path[-1] != eind:
        response = requests.get(BASE_URL + path[-1])
        scraper = bs4.BeautifulSoup(response.text, "html.parser")
        body = scraper.find("div", {"id": "bodyContent"})
        path.append(find_link(body)[6:])
    return path


# Lees data verstuurd door JavaScript
parameters = cgi.FieldStorage()
# data = json.loads(parameters.getvalue("data"))
# waarde = parameters.getvalue("waarde")
begin = parameters.getvalue("begin")
eind = parameters.getvalue("eind")

# Bereken te verzenden data
# nieuwe_lijst = data["lijst"] + [waarde]
# nieuwe_data = {"lijst": nieuwe_lijst}
path = {"path": get_path(begin, eind)}

# Stuur antwoord terug
print("Content-Type: application/json")
print()  # Lege lijn na headers
print(json.dumps(path))
