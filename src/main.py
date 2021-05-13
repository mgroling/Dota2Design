from interface import Dota2DesignInterface
from functions import *
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


if __name__ == "__main__":
    # Dota2DesignInterface()

    # ["players"][0]["purchase_time"] ["dire_team"]["logo_url"]
    dic = getMatchDictionary(5990966909)["players"][0]

    # print(dic)
    for key in dic.keys():
        print(key)

    # path to hero ids: I:/SteamLibrary/steamapps/common/dota 2 beta/game/dota/scripts/npc/npc_heroes.txt