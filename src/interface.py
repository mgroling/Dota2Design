from functions import *
import tkinter as tk


class Dota2DesignInterface:
    def __init__(self):
        root = tk.Tk()
        root.resizable(False, False)
        frame = tk.Frame(root, width=600, height=400, background="#2c2c2c")

        for i in range(5):
            label = tk.Label(
                text="Game " + str(i + 1),
                font=("Helvetica", 20),
                bg="#2c2c2c",
                fg="#e1612d",
            )
            label.place(x=20, y=20 + i * 50)

        frame.pack()

        # label = tk.Label(root, text="Match Id:").grid(row=0)
        # entry = tk.Entry(root)
        # entry.grid(row=0, column=1)
        # button = tk.Button(
        #     root, text="Enter", command=lambda: createImages(entry.get())
        # ).grid(row=1, sticky=tk.W, pady=4)

        root.mainloop()


if __name__ == "__main__":
    Dota2DesignInterface()