from requests import get
from bs4 import BeautifulSoup

class SlovnikException(Exception):
    def __init__(self, zprava: str = "Něco se podělalo ¯\\_(ツ)_/¯"):
        self.message = zprava
        super().__init__(self.message)

class StrankaNenalezena(SlovnikException):
    def __init__(self, code: int = None):
        self.message = "Nepodařilo se nám načíst stránku."
        if code != None:
            self.message += f"(Error kód: {code})"
        super().__init__(zprava=self.message)

class Slovo:
    # Časem řidám další parametry
    def __init__(self, slovo, deleni, rod, vyznam, priklady):
        self.slovo = slovo
        self.deleni = deleni
        self.rod = rod
        self.vyznam = vyznam
        self.priklady = priklady

    def __str__(self):
        return self.slovo

class Slovnik:
    def __init__(self):
        self.url = "https://prirucka.ujc.cas.cz/?slovo="
    def hledat(self, slovo: str) -> list:
        url = self.getURL(slovo)
        html = self.getHTLM(url)
        slovo = self.parseHTML(html)
        if type(slovo) == list:
            slova = []
            for slovo_url in slovo:
                html = self.getHTLM(slovo_url)
                slova.append(self.parseHTML(html))
            return slova
        elif type(slovo) == Slovo:
            return [slovo]
        elif type(slovo) == None:
            return slovo

    def getURL(self, slovo: str) -> str:
        return self.url + slovo

    def getHTLM(self, url: str):
        res = get(url)
        if res.status_code == 200:
            return res.content
        else:
            return StrankaNenalezena(code=res.status_code)

    def parseHTML(self, html):
        parsed = BeautifulSoup(html, 'html.parser')
        main = parsed.html.body.find_all("div", attrs={"id": "content"})[0].find_all("div", class_="", attrs={"id": ""})

        if len(main) < 1:
            return None

        main = main[0]

        urls = []
        linky = main.find_all("span", class_="odsazeno")
        for link in linky:
            urls.append(link.find("a")["href"])
        if len(urls) > 0:
            return urls

        polozky = main.find_all("p", class_="polozky")
        slovo = main.find_all("div", class_="hlavicka")[0].text.replace("\n", "")
        deleni = None
        rod = None
        vyznam = None
        priklady = None
        for polozka in polozky:
            # Odstaníme link
            if polozka.sup != None:
                polozka.sup.decompose()

            # Identifikujeme příslušný text
            txt = polozka.text
            if txt.startswith("dělení: "):
                deleni = txt.replace("dělení: ", "")
            elif txt.startswith("rod: "):
                rod = txt.replace("rod: ", "")
            elif txt.startswith("význam: "):
                vyznam = txt.replace("význam: ", "")
            elif txt.startswith("příklady: "):
                priklady = txt.replace("příklady: ", "")
        res = Slovo(slovo, deleni, rod, vyznam, priklady)
        return res