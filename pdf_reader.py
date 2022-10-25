from concurrent.futures import BrokenExecutor
import glob
import os
import camelot
import csv
import dataBaseManipulator

from pandas import array


def tableTypeCheck(firstRow) -> str:
    for cell in firstRow:
        if (cell == "But" or cell == "Ass"):
            return "goalTable"
        elif (cell == "Equipe A" or cell == "Equipe B"):
            return "presTable"
        elif (cell == "Code"):
            return "foolTable"
        elif (cell == "Joueurs"):
            return "awayTeamTable"
        elif (cell == "Signature"):
            return "refereeTable"


def teamStatCheck(table1, table2, isGameWin) -> array:
    if (isGameWin):
        if (len(table1) > len(table2)):
            return table1
        else:
            return table2
    else:
        if (len(table1) < len(table2)):
            return table1
        else:
            return table2


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


def playerStat(teamStats) -> array:
    playersStats = [[0, 0, 0]]
    alreadyInTable = False
    for rowsTeam in teamStats[1:]:
        if (rowsTeam[1] != ''):
            alreadyInTable = False
            goal = int(rowsTeam[1])
            print("new goal found : " + str(goal))
            for rowsPlayers in playersStats:
                if goal in rowsPlayers:
                    rowsPlayers[0] += 1
                    print("Goal added")
                    alreadyInTable = True
                    break
                else:
                    continue
            if not alreadyInTable:
                try:
                    newLayer = [0, 0, goal]
                    newLayer[0] += 1
                    playersStats.append(newLayer)
                except TypeError as err:
                    print(err)
                print("new layer created for a goal")
                alreadyInTable = False
        if (rowsTeam[2] != ''):
            alreadyInTable = False
            assist = int(rowsTeam[2])
            print("new assist found : " + str(assist))
            for rowsPlayers in playersStats:
                if assist in rowsPlayers:
                    rowsPlayers[1] += 1
                    print("assist Added")
                    alreadyInTable = True
                    break
                else:
                    continue
            if not alreadyInTable:
                print("new row in creation")
                try:
                    newLayer = [0, 0, assist]
                    newLayer[1] += 1
                    playersStats.append(newLayer)
                except TypeError as err:
                    print(err)
                print("new layer created for an assist")
                alreadyInTable = False
    playersStats.pop(0)
    return playersStats


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
rempartStat = []
awayStat = []
inputRight = True


while (inputRight):
    inp = input("Did \"Les Remparts\" won the game ? (Y/N)\n")
    if (inp == "Y" or inp == "N"):
        if (inp == "Y"):
            isGameWin = True
        else:
            isGameWin = False
        inputRight = False
    else:
        print("Please enter Y or N")


for table in data:
    fileName = './temporary/table'+str(nbTable)+'.csv'
    table.to_csv(fileName)
    datas = tableCreater(fileName)
    if (teamRempartCheck(datas)):
        datas.insert(0, "Les Remparts")
        datas.pop(1)
        datas = nameArrayStyle(datas)
        rempartArrayTemp = datas
    else:
        datas.insert(0, tableTypeCheck(datas[0]))
        datas.pop(1)
    if (datas[0] == "Les Remparts"):
        dataBaseManipulator.AddTeamTableInDb(datas)
    if (datas[0] == "goalTable"):
        if (not rempartStat):
            rempartStat = datas
            rempartStat.pop(len(rempartStat)-1)
        else:
            awayStat = datas
            awayStat.pop(len(awayStat)-1)
    for row in datas:
        print(row)
    print("\n\n\n")
    nbTable += 1
rempartStat = teamStatCheck(rempartStat, awayStat, isGameWin)
playersStats = playerStat(rempartStat)
dataBaseManipulator.AddGoalAssistInDB(playersStats)

print("there is " + str(nbTable) + " table in this pdf")
