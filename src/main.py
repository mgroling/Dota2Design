from functions_summarize import *

# from functions_photoshop import *

if __name__ == "__main__":
    # pics, texts = getAfterGameStatistics(6227305557)

    # doc = openSession(os.getcwd() + "/After_Game_Statistics_25_10_2021.psd")

    # for key, value in pics.items():
    #     changeImage(doc, key, value)

    # for key, value in texts.items():
    #     changeText(doc, key, value)

    doc = openSession(os.getcwd() + "/After_Game_Statistics_25_10_2021.psd")

    # doc.artLayers["radiant_networth"].textItem.position = [300, 300]
    print(doc.artLayers["radiant_networth"].textItem)
