from codecs import namereplace_errors
from distutils.command.build_scripts import first_line_re
import glob
import os
from unicodedata import name
import camelot
import csv
import dataBaseManipulator

from pandas import array


def tableTypeCheck(firstRow) -> str:
    for cell in firstRow:
        if (cell == "But" or cell == "Ass"):
            return "goalTable"
        elif (cell == "Equipe A" or cell == "Equipe B"):
            return "presTabel"
        elif (cell == "Code"):
            return "foolTable"
        elif (cell == "Joueurs"):
            return "teamTable"
        elif (cell == "Signature"):
            return "refereeTable"


def isEmptyCheck(row) -> bool:
    emptyCell = 0
    for cell in row:
        if (cell == ''):
            emptyCell += 1
            if (emptyCell == len(row)):
                return True
    return False


def teamRempartCheck(table) -> bool:
    for row in table:
        for i in range(len(row)):
            if (row[i] == "François LouÉ" or row[i] == "Kilian Hauray"):
                return True
    return False


def uselessRow(row) -> bool:
    for cell in row:
        if (cell == "Officiels d'équipe"):
            return True
    return False


def tableCreater(file) -> array:
    dataTable = []
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            isEmpty = isEmptyCheck(row)
            if (isEmpty):
                continue
            elif (uselessRow(row)):
                break
            else:
                dataTable.append(row)
    return dataTable


def nameArrayStyle(table):
    for rows in table[1:]:
        nameSplit = rows[2].split()
        for names in nameSplit:
            names = names.replace("É", "é")
            names = names.replace("Ê", "ê")
            rows.append(names)
        rows.remove(rows[2])
    return table


list_of_files = glob.glob("./feuille_de_matchs/*")
latest_file = max(list_of_files, key=os.path.getctime)
data = camelot.read_pdf(latest_file)
nbTable = 0
for table in data:
    fileName = './temporary/table'+str(nbTable)+'.csv'
    table.to_csv(fileName)
    datas = tableCreater(fileName)
    if (teamRempartCheck(datas)):
        datas.insert(0, "Les Remparts")
        datas.pop(1)
        datas = nameArrayStyle(datas)
    else:
        datas.insert(0, tableTypeCheck(datas[0]))
        datas.pop(1)
    if (datas[0] == "Les Remparts"):
        dataBaseManipulator.teamTable(datas)
    for row in datas:
        print(row)
    print("\n\n\n")
    nbTable += 1

print(tableTypeCheck(datas[0]))
print("there is " + str(nbTable) + " table in this pdf")
