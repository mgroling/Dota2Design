from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import json
import win32com.client
import os


def removeChars(string):
    copy = [char for char in string]
    i = 0
    for char in string:
        if not (
            (ord(char) >= 48 and ord(char) <= 57)
            or (ord(char) >= 65 and ord(char) <= 90)
            or (ord(char) >= 97 and ord(char) <= 122)
        ):
            copy = copy[:i] + copy[i + 1 :]
        else:
            i += 1
    out = ""
    for char in copy:
        out += char

    return out


def getMatchDictionary(match_id):
    req = Request(
        "https://api.opendota.com/api/matches/" + str(match_id),
        headers={"User-Agent": "Mozilla/5.0"},
    )
    page_html = urlopen(req).read()
    page_soup = soup(page_html, "html.parser")
    return json.loads(str(page_soup))


def getPlayerInfo(matchDictionary, id):
    player = matchDictionary["players"][id]

    return {
        "nickname": removeChars(player["name"]),
        "level": player["level"],
        "kills": player["kills"],
        "assists": player["assists"],
        "deaths": player["deaths"],
        "gpm": player["gold_per_min"],
        "xpm": player["xp_per_min"],
        "Networth": player["net_worth"],
        "buildingDamage": player["tower_damage"],
        "heroDamage": player["hero_damage"],
        "heroHealing": player["hero_healing"],
    }


def createImages(match_id):
    dic = getMatchDictionary(match_id)

    psApp = win32com.client.Dispatch("Photoshop.Application")
    doc = psApp.Open(os.getcwd() + "\Base_2.psd")

    elements = [
        "nickname",
        "level",
        "kills",
        "deaths",
        "gpm",
        "xpm",
        "buildingDamage",
        "heroDamage",
        "heroHealing",
    ]
    players = [getPlayerInfo(dic, i) for i in range(10)]

    for elem in elements:
        doc.ArtLayers[elem].TextItem.contents = str(players[1][elem])
