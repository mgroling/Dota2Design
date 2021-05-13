from functions import *
import tkinter as tk
from PIL import Image, ImageTk
import os
import pandas as pd
import numpy


def refreshDropDownMenu(dropDownMenu, choices, var):
    dropDownMenu["menu"].delete(0, "end")
    for choice in choices:
        dropDownMenu["menu"].add_command(label=choice, command=tk._setit(var, choice))


class Dota2DesignInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Dota2Design")
        canvas = tk.Canvas(self.root, width=600, height=400)

        img = ImageTk.PhotoImage(Image.open("data/gui_img/Background.png"))
        canvas.background = img
        bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)

        for i in range(5):
            canvas.create_text(
                70,
                100 + i * 40,
                text="Game " + str(i + 1),
                font=("Helvetica", 15, "bold"),
                fill="#ffffff",
            )

        entries = []
        for i in range(5):
            entries.append(
                tk.Entry(
                    font=("Helvetica", 16, "bold"),
                    bg="#ff5005",
                    fg="#ffffff",
                )
            )
            entries[-1].place(x=130, y=85 + i * 40, height=30, width=210)

        photoButton1 = ImageTk.PhotoImage(Image.open("data/gui_img/Load Games.png"))
        loadMatchesButton = tk.Button(
            command=lambda: self.getPlayerNames([entry.get() for entry in entries]),
            image=photoButton1,
        )
        loadMatchesButton.place(x=35, y=300, width=304, height=33)

        self.variablePlayer = tk.StringVar(self.root)
        self.variablePlayer.set(None)
        self.dropDownBoxPlayer = tk.OptionMenu(self.root, self.variablePlayer, None)
        self.dropDownBoxPlayer.config(bg="#141517")
        self.dropDownBoxPlayer.place(x=350, y=125, width=212, height=30)

        canvas.create_text(
            460,
            100,
            text="Choose Player",
            font=("Helvetica", 16, "bold"),
            fill="#ffffff",
        )
        canvas.create_text(
            460,
            220,
            text="Choose Game",
            font=("Helvetica", 16, "bold"),
            fill="#ffffff",
        )

        self.variableGame = tk.StringVar(self.root)
        self.variableGame.set(None)
        self.dropDownBoxGame = tk.OptionMenu(
            self.root, self.variableGame, "1", "2", "3", "4", "5", "All"
        )
        self.dropDownBoxGame.config(bg="#141517")
        self.dropDownBoxGame.place(x=350, y=245, width=212, height=30)

        photoButton2 = ImageTk.PhotoImage(Image.open("data/gui_img/Create Graphic.png"))
        loadMatchesButton = tk.Button(
            command=lambda: createImages(
                self.match_dics,
                self.variableGame.get(),
                self.players.index(self.variablePlayer.get()),
                self.players,
            ),
            image=photoButton2,
        )
        loadMatchesButton.place(x=350, y=300, width=212, height=33)

        canvas.pack()
        self.root.mainloop()

    def getPlayerNames(self, match_ids):
        match_ids = [x for x in match_ids if x]
        self.match_dics = [getMatchDictionary(match_id) for match_id in match_ids]
        self.players = [getPlayerNames(dic) for dic in self.match_dics]

        self.players = validatePlayers(self.players)
        self.players.append("All")

        refreshDropDownMenu(self.dropDownBoxPlayer, self.players, self.variablePlayer)


if __name__ == "__main__":
    Dota2DesignInterface()
    # df = pd.read_csv("data/items_id.csv", sep=";").to_numpy()

    # d = loadConfig("data/item_img/item_mapping.json")
    # d = {int(k): v for k, v in d.items()}
    # print(dic)
    # res = dict((v, float(k)) for k, v in dic.items())
    # print(d)
    # saveConfig("data/item_img/item_mapping.json", d)

    # item_mapping = {}
    # for i in range(len(df)):
    #     item_mapping[df[i][1][5:]] = df[i][3]

    # saveConfig("data/item_img/item_mapping.json", item_mapping)

    # 5990966909

    # for path in os.listdir("data/item_img/"):
    # img = Image.open("data/item_img/0.png")
    # img = img.resize(
    #     (90, 66), Image.ANTIALIAS
    # )
    # img.save("data/item_img/0.png")