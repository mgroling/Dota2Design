from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from PIL import Image, ImageTk
import json
import os
import photoshop.api as ps
from photoshop import Session
import requests
import pandas as pd
import numpy as np


def saveConfig(path, dic):
    with open(path, "w+") as f:
        json.dump(dic, f)


def loadConfig(path):
    with open(path, "r") as f:
        return json.load(f)


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


def validatePlayers(players):
    players = [sorted(elem) for elem in players]
    for j in range(len(players) - 1):
        for i in range(len(players[j])):
            if players[j][i] != players[j + 1][i]:
                print("player names inconsistent")
                break

    return players[0]


def getMatchDictionary(match_id):
    req = Request(
        "https://api.opendota.com/api/matches/" + str(match_id),
        headers={"User-Agent": "Mozilla/5.0"},
    )
    page_html = urlopen(req).read()
    page_soup = soup(page_html, "html.parser")
    dic = json.loads(str(page_soup))
    players = getPlayerNames(dic)
    dic["players"] = [x for _, x in sorted(zip(players, dic["players"]))]

    return dic


def getPlayerNames(matchDictionary):
    return [
        removeChars(matchDictionary["players"][i]["name"])
        for i in range(len(matchDictionary["players"]))
    ]


def changeImage(doc, layer_name, image_path):
    doc.activeLayer = doc.ArtLayers[layer_name]
    with Session() as pss:
        replace_contents = pss.app.stringIDToTypeID("placedLayerReplaceContents")
        desc = pss.ActionDescriptor
        idnull = pss.app.charIDToTypeID("null")
        desc.putPath(idnull, image_path)
        pss.app.executeAction(replace_contents, desc)


def getPlayerInfo(matchDictionary, id):
    player = matchDictionary["players"][id]

    return {
        "nickname": removeChars(player["name"]),
        "heroId": player["hero_id"],
        "level": player["level"],
        "kills": player["kills"],
        "assists": player["assists"],
        "deaths": player["deaths"],
        "gpm": player["gold_per_min"],
        "xpm": player["xp_per_min"],
        "networth": player["net_worth"],
        "buildingDamage": player["tower_damage"],
        "heroDamage": player["hero_damage"],
        "heroHealing": player["hero_healing"],
        "item0": player["item_0"],
        "item1": player["item_1"],
        "item2": player["item_2"],
        "item3": player["item_3"],
        "item4": player["item_4"],
        "item5": player["item_5"],
        "purchase_time": player["purchase_time"],
    }


def convertSecToMin(seconds):
    if seconds < 0:
        return "00:00"
    else:
        return "{:02d}".format(seconds // 60) + ":" + "{:02d}".format(int(seconds % 60))


def getItemTimings(player_dic):
    mapping = loadConfig("data/item_img/item_mapping.json")

    out = []
    for i in range(6):
        item_id = player_dic["item{}".format(i)]
        if item_id != 0:
            item_name = mapping[str(float(item_id))]
            if not item_name in ["aegis", "cheese", "refresher_shard"]:
                time = player_dic["purchase_time"][item_name]
                out.append([item_id, time])
            else:
                out.append([item_id, np.inf])
        else:
            out.append([item_id, np.inf])

    out.sort(key=lambda x: x[1])
    for i in range(len(out)):
        if out[i][1] != np.inf:
            out[i][1] = convertSecToMin(out[i][1])
        else:
            out[i][1] = "-"

    return out

def createImages(match_dictionaries, games, players, player_names):
    if games == "All":
        dics_to_iterate_over = match_dictionaries
    else:
        dics_to_iterate_over = [match_dictionaries[int(games) - 1]]
    if players == 10:
        players_to_iterate_over = [i for i in range(10)]
    else:
        players_to_iterate_over = [int(players)]

    app = ps.Application()
    doc = app.open(os.getcwd() + "/player_performance_base.psd")

    elements = [
        "nickname",
        "level",
        "kills",
        "deaths",
        "assists",
        "gpm",
        "xpm",
        "buildingDamage",
        "heroDamage",
        "heroHealing",
        "networth",
    ]

    team1, team2 = match_dictionaries[0]["radiant_team"]["name"].replace(" ", ""), match_dictionaries[0]["dire_team"]["name"].replace(" ", "")
    if os.path.isfile(os.getcwd() + "/data/team_logos/{}.png".format(team1)):
        changeImage(doc, "team_logo_1", os.getcwd() + "/data/team_logos/{}.png".format(team1))
    else:
        changeImage(doc, "team_logo_1", os.getcwd() + "/data/team_logos/empty_logo.png")

    if os.path.isfile(os.getcwd() + "/data/team_logos/{}.png".format(team2)):
        changeImage(doc, "team_logo_2", os.getcwd() + "/data/team_logos/{}.png".format(team2))
    else:
        changeImage(doc, "team_logo_2", os.getcwd() + "/data/team_logos/empty_logo.png")

    doc.ArtLayers["team_1"].TextItem.contents = team1
    doc.ArtLayers["team_2"].TextItem.contents = team2

    for i, game in enumerate(dics_to_iterate_over):
        doc.ArtLayers["matchID"].TextItem.contents = str(game["match_id"])
        doc.ArtLayers["game"].TextItem.contents = games
        doc.ArtLayers["duration"].TextItem.contents = (
            convertSecToMin(match_dictionaries[int(games) - 1]["duration"]) + " MIN"
        )
        for player in players_to_iterate_over:
            player_game_dic = getPlayerInfo(game, player)

            for elem in elements:
                doc.ArtLayers[elem].TextItem.contents = str(player_game_dic[elem])

            # change hero image
            changeImage(
                doc,
                "Hero",
                os.getcwd() + "/data/hero_img/{}.png".format(player_game_dic["heroId"]),
            )

            items = getItemTimings(player_game_dic)
            for j in range(len(items)):
                changeImage(
                    doc,
                    "item_{}".format(j + 1),
                    os.getcwd() + "/data/item_img/{}.png".format(items[j][0]),
                )
                doc.ArtLayers["item_{}_time".format(j + 1)].TextItem.contents = str(
                    items[j][1]
                )

            doc.saveAs(
                os.getcwd()
                + "/results/game_"
                + str(i)
                + "_player_"
                + player_names[player]
                + ".png",
                ps.PNGSaveOptions(),
                True,
            )
