import bs4
import requests


class Path:
    def __init__(self, begin, end, language) -> None:
        self.path = []
        self.begin = begin
        self.end = end
        self.base_url = f"https://{language}.wikipedia.org"
        self.status_message = "not constructed"

    def is_valid(self, link, paragraph) -> bool:
        """Checkt of de link wel tot de juiste criteria behoort:
        enkel reguliere link is toegestaan en mag niet tussen haakjes staan."""

        search_area = paragraph[0 : paragraph.find(link.text)]

        return (
            search_area.count("(") <= search_area.count(")")
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

    def get_scraper(self, url):
        """Retourneert het soup object."""

        try:
            response = requests.get(self.base_url + url)
        except requests.exceptions.ConnectionError:
            self.status_message = "Unable to reach site."
        else:
            if response.status_code == 200:
                scraper = bs4.BeautifulSoup(response.text, "html.parser")
                return scraper
            elif response.status_code == 404:
                self.status_message = f"Page {self.end} not found."

    def construct_path(self) -> None:
        """Construeert een pad van start naar stop en slaat het op."""

        current_link = "/wiki/" + self.begin

        scraper = self.get_scraper("/wiki/" + self.end)
        if not scraper:
            return

        end_title = scraper.find("h1", {"id": "firstHeading"}).text
        stop = False
        while not stop:
            scraper = self.get_scraper(current_link)

            if scraper:
                title = scraper.find("h1", {"id": "firstHeading"}).text
                if title == end_title:
                    self.status_message = "success"
                    self.path.append(self.end)
                    stop = True
                elif title in self.path:
                    self.status_message = f"Cycle detected at page {title}."
                    stop = True
                else:
                    self.path.append(title)
                    body = scraper.find("div", {"id": "bodyContent"})
                    current_link = self.find_link(body)

                    if not current_link:
                        self.status_message = f"No link found in page: {title}."
                        stop = True
            else:
                stop = True
