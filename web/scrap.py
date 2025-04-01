# scrap.py
import requests
from bs4 import BeautifulSoup
import state


def fetch_fide_rating():
    url = "https://ratings.fide.com/profile/1503014"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    standard_block = soup.find("div", class_="profile-standart")
    rating = standard_block.find("p").text.strip() if standard_block else "Non trouvé"

    state.FIDE_ELO = rating
