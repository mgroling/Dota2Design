import os
from numpy import mat

from functions_api import *
from functions_plot import *


def getAfterGameStatistics(match_id):
    match_dic = getMatchDic(match_id)
    cwd = os.getcwd()

    pictures = {}
    # Picks and Bans
    picks_bans = getPickBan(match_dic)
    side = ["_radiant", "_dire"]
    for pick in picks_bans["picks"]:
        pictures["pick_" + str(pick["order"]) + side[pick["team"]]] = (
            cwd + "/data/hero_img/" + str(pick["hero_id"]) + ".png"
        )
    for ban in picks_bans["bans"]:
        pictures["ban_" + str(ban["order"]) + side[ban["team"]]] = (
            cwd + "/data/hero_img/" + str(ban["hero_id"]) + ".png"
        )

    # Networth Graph
    path = cwd + "/data/temp/net.png"
    adv = getRadiantGoldAdvantage(match_dic)
    plotAdv(adv, path)
    pictures["net_worth_graph"] = path

    # Xp Graph
    path = cwd + "/data/temp/xp.png"
    adv = getRadiantXpAdvantage(match_dic)
    plotAdv(adv, path)
    pictures["experience_graph"] = path

    text_fields = {}
    # Team stats
    player_info = getPlayerInfo(match_dic)
    attributes = ["networth", "aegis", "hero_damage", "hero_healing", "building_damage"]
    for side in ["radiant_", "dire_"]:
        text_fields[side + "kda"] = "{}/{}/{}".format(
            player_info[side + "kills"],
            player_info[side + "deaths"],
            player_info[side + "assists"],
        )

        text_fields[side + "lh_dn"] = "{}/{}".format(
            player_info[side + "last_hits"], player_info[side + "denies"]
        )

        for attr in attributes:
            text_fields[side + attr] = str(player_info[side + attr])

    # Tower
    tower_status = getTowerStatus(match_dic)
    text_fields["radiant_tower"] = str(11 - sum(tower_status["dire"].values()))
    text_fields["dire_tower"] = str(11 - sum(tower_status["radiant"].values()))

    # League Info
    series_info = getSeriesLeagueInfo(match_dic)
    radiant, dire = (
        series_info[series_info["radiant_team_id"]],
        series_info[series_info["dire_team_id"]],
    )
    text_fields["game_number"] = "GAME " + str(series_info["number_game"])
    text_fields["game_score"] = "{} - {}".format(radiant["score"], dire["score"])
    text_fields["radiant_teamname"] = radiant["name"]
    text_fields["dire_teamname"] = dire["name"]
    text_fields["radiant_victory_defeated"] = (
        "VICTORY" if series_info["radiant_win"] else "DEFEATED"
    )
    text_fields["dire_victory_defeated"] = (
        "DEFEATED" if series_info["radiant_win"] else "VICTORY"
    )

    return pictures, text_fields
