import os
import photoshop.api as ps
from photoshop import Session


def changeImage(doc, layer_name, image_path):
    doc.activeLayer = doc.ArtLayers[layer_name]
    with Session() as pss:
        replace_contents = pss.app.stringIDToTypeID("placedLayerReplaceContents")
        desc = pss.ActionDescriptor
        idnull = pss.app.charIDToTypeID("null")
        desc.putPath(idnull, image_path)
        pss.app.executeAction(replace_contents, desc)


def changeText(doc, layer_name, text):
    doc.ArtLayers[layer_name].TextItem.contents = str(text)


def openSession(path):
    app = ps.Application()
    doc = app.open(path)

    return doc


def saveDocument(doc, path):
    doc.saveAs(
        path,
        ps.PNGSaveOptions(),
        True,
    )
