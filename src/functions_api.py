from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import json

from numpy import mat


def getLeagueDic(league_id):
    req = Request(
        "https://api.opendota.com/api/leagues/{}/matches".format(league_id),
        headers={"User-Agent": "Mozilla/5.0"},
    )
    page_html = urlopen(req).read()
    page_soup = soup(page_html, "html.parser")
    return json.loads(str(page_soup))


def getLeagueName(league_id):
    req = Request(
        "https://api.opendota.com/api/leagues/{}".format(league_id),
        headers={"User-Agent": "Mozilla/5.0"},
    )
    page_html = urlopen(req).read()
    page_soup = soup(page_html, "html.parser")
    return json.loads(str(page_soup))["name"]


def getMatchDic(match_id):
    req = Request(
        "https://api.opendota.com/api/matches/{}".format(match_id),
        headers={"User-Agent": "Mozilla/5.0"},
    )
    page_html = urlopen(req).read()
    page_soup = soup(page_html, "html.parser")
    return json.loads(str(page_soup))


def convertSecToMin(seconds):
    if seconds < 0:
        return "00:00"
    else:
        return "{:02d}".format(seconds // 60) + ":" + "{:02d}".format(int(seconds % 60))


def getPlayerInfo(match_dic):
    out = {"radiant_players": [], "dire_players": []}
    for player in match_dic["players"]:
        if bool(player["isRadiant"]):
            to_append = "radiant_players"
        else:
            to_append = "dire_players"
        out[to_append].append(
            {
                "nickname": player["name"],
                "hero_id": player["hero_id"],
                "kills": player["kills"],
                "deaths": player["deaths"],
                "assists": player["assists"],
                "hero_damage": player["hero_damage"],
                "hero_healing": player["hero_healing"],
                "building_damage": player["tower_damage"],
                "networth": player["net_worth"],
                "xp": player["total_xp"],
                "last_hits": player["last_hits"],
                "denies": player["denies"],
                "roshan_kills": player["roshan_kills"],
                "aegis": 0,
            }
        )

    for msg in match_dic["objectives"]:
        if msg["type"] == "CHAT_MESSAGE_AEGIS":
            if msg["slot"] < 5:
                out["radiant_players"][int(msg["slot"])]["aegis"] += 1
            else:
                out["dire_players"][int(msg["slot"]) - 5]["aegis"] += 1

    team_attributes = [
        "kills",
        "deaths",
        "assists",
        "hero_damage",
        "hero_healing",
        "building_damage",
        "networth",
        "xp",
        "last_hits",
        "denies",
        "roshan_kills",
        "aegis",
    ]
    for side in ["radiant_", "dire_"]:
        for attribute in team_attributes:
            out[side + attribute] = sum(
                [elem[attribute] for elem in out[side + "players"]]
            )

    return out


def getPickBan(match_dic):
    out = {"picks": [], "bans": []}
    p_num, b_num = [0, 0], [0, 0]
    for pick_ban in match_dic["picks_bans"]:
        if bool(pick_ban["is_pick"]):
            p_num[pick_ban["team"]] += 1
            out["picks"].append(
                {
                    "team": pick_ban["team"],
                    "hero_id": pick_ban["hero_id"],
                    "order": p_num[pick_ban["team"]],
                }
            )
        else:
            b_num[pick_ban["team"]] += 1
            out["bans"].append(
                {
                    "team": pick_ban["team"],
                    "hero_id": pick_ban["hero_id"],
                    "order": b_num[pick_ban["team"]],
                }
            )

    return out


def getSeriesLeagueInfo(match_dic):
    league_dic = getLeagueDic(match_dic["league"]["leagueid"])
    series_games = [
        elem for elem in league_dic if elem["series_id"] == match_dic["series_id"]
    ]
    out = {
        "league_name": getLeagueName(match_dic["league"]["leagueid"]),
        "series_type": match_dic["series_type"],
        "number_game": len(
            [
                elem
                for elem in series_games
                if elem["start_time"] <= match_dic["start_time"]
            ]
        ),
        "radiant_team_id": match_dic["radiant_team"]["team_id"],
        "dire_team_id": match_dic["dire_team"]["team_id"],
        "radiant_win": match_dic["radiant_win"],
        match_dic["radiant_team"]["team_id"]: {
            "name": match_dic["radiant_team"]["name"],
            "score": 0,
        },
        match_dic["dire_team"]["team_id"]: {
            "name": match_dic["dire_team"]["name"],
            "score": 0,
        },
    }
    for game in series_games:
        if game["radiant_win"]:
            out[game["radiant_team_id"]]["score"] += 1
        else:
            out[game["dire_team_id"]]["score"] += 1

    return out


def getTowerStatus(match_dic):
    out = {}
    get_bin = lambda x, n: format(x, "b").zfill(n)
    for side in ["radiant", "dire"]:
        tower = [
            "ancient_top",
            "ancient_bottom",
            "tier_3_bottom",
            "tier_2_bottom",
            "tier_1_bottom",
            "tier_3_middle",
            "tier_2_middle",
            "tier_1_middle",
            "tier_3_top",
            "tier_2_top",
            "tier_1_top",
        ]
        status = get_bin(match_dic["tower_status_" + side], 11)
        out[side] = {}
        for i, bit in enumerate(status):
            out[side][tower[i]] = int(bit)  # 1 is alive, 0 is dead

    return out


def getRadiantGoldAdvantage(match_dic):
    return match_dic["radiant_gold_adv"]


def getRadiantXpAdvantage(match_dic):
    return match_dic["radiant_xp_adv"]


def getGameLength(match_dic):
    return convertSecToMin(match_dic["duration"])
