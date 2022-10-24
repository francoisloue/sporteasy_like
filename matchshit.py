"""
-Récupérer la feuille de match par téléchargement du fichier directement a partir du lien (forme du lien https://rolskanet.fr/sportif/live/(à demandé à l'utilisateur)/rapport)
-Enregistrer le fichier dans un dossier spécial (en local ou sur répo?)
"""

import requests
import PyPDF2
import os


def URLFormat() -> str:
    URL = "https://rolskanet.fr/sportif/live/ID/rapport"
    isInputValid = False
    while (isInputValid == False):
        matchId = input(
            "Please enter the match ID (5 digits format ex: 00000) : ")
        if (len(matchId) == 5 and matchId.isnumeric()):
            isInputValid = True
            URL = URL.replace("ID", matchId)
        else:
            print("Please enter a valid ID")
    return URL


def DowloadMatchShit(URL):
    try:
        response = requests.get(URL)
    except requests.exceptions.request.RequestException as e:
        raise SystemExit(e)
    URLarray = URL.split('/')
    for element in URLarray:
        if (len(element) == 5 and element.isnumeric()):
            matchID = element
            file = "./feuille_de_matchs/match_" + matchID + ".pdf"
            fileName = "match_"+matchID
    try:
        open(file, "wb").write(response.content)
        try:
            PyPDF2.PdfFileReader(open(file, "rb"))
        except Exception:
            os.remove(file)
            print("Invalid match ID, please retry with another ID\n" +
                  fileName+" has been removed")
    except IOError:
        print("Could not read or write properly:", fileName)


DowloadMatchShit(URLFormat())
