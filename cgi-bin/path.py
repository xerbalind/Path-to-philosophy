import bs4
import requests
import utils


class Path:
    def __init__(self, begin, end, language) -> None:
        self.path = []
        self.begin = begin
        self.end = end
        self.base_url = f"https://{language}.wikipedia.org"
        self.status_message = "nothing done"

    def is_valid(self, link, paragraph) -> bool:
        """Checkt of de link wel tot de juiste criteria behoort:
        enkel reguliere link is toegestaan en mag niet tussen haakjes zijn."""

        return (
            not utils.between_braces(0, paragraph.find(link.text), paragraph)
            and ":" not in link["href"]
            and link["href"].startswith("/wiki/")
        )

    def find_link(self, body) -> str:
        """Vind de eerst goede link binnen een p tag in de body.
        En retourneert het adres."""

        for paragraph in body.find_all("p"):
            for link in paragraph.find_all("a", href=True):
                if self.is_valid(link, paragraph.text):
                    return link["href"]

        return ""

    def construct_path(self) -> None:
        """Construeert een pad van start naar stop en slaat het op."""

        current_link = "/wiki/" + self.begin

        stop = False
        while not stop:

            response = requests.get(self.base_url + current_link)
            scraper = bs4.BeautifulSoup(response.text, "html.parser")

            title = scraper.find("h1", {"id": "firstHeading"}).text
            if title.lower() == self.end.lower():
                self.status_message = "success"
                stop = True
            if title in self.path:
                self.status_message = f"Cycle detected at page {title}."
                stop = True

            self.path.append(title)
            body = scraper.find("div", {"id": "bodyContent"})
            current_link = self.find_link(body)

            if not current_link:
                self.status_message = f"No link found in page: {title}."
                stop = True
