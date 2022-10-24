import sqlite3
from tabnanny import check


def dbConnexion():
    con = sqlite3.connect("./RempartStat")
    return con


def teamTable(table):
    try:
        con = dbConnexion()
        cursor = con.cursor()
        print("Successfuly accessed database")
        sqlCommand = """INSERT INTO Players (LicenceNumber, Lastname, Name, Number) VALUES ({}, '{}', '{}', {})"""
        rowCount = 1
        for row in table[1:]:
            if (not alreadyInDB(row[2])):
                sqlCommandTempon = sqlCommand.format(
                    row[1], row[4], row[3], row[2])
                print("This command should be executed: " + sqlCommandTempon)
                count = cursor.execute(sqlCommandTempon)
                con.commit()
                print("Row : " + str(rowCount) +
                      " has been successfuly commited")
                rowCount += 1
            else:
                print("Row "+str(rowCount)+" was already in database")
                rowCount += 1
                continue
        print("Successfuly commited every row")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert datas into database ", error)
    finally:
        if con:
            con.close()
            print("The sqlite connection is closed !")


def alreadyInDB(number) -> bool:
    try:
        con = dbConnexion()
        cursor = con.cursor()
        cursor.execute(
            'SELECT Number FROM Players WHERE Number="%s"' % (number))
        check = cursor.fetchall()
        print(check[0])
        if (check[0] == "("+str(number)+", )"):
            return True
        else:
            cursor.close()
    except sqlite3.Error as error:
        print("Failed to check if Player already exist in database ", error)
    finally:
        if con:
            con.close()


def deleteRecord():
    try:
        sqliteConnection = dbConnexion()
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        sql_delete_query = """DELETE from Players"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        print("Record deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


if (alreadyInDB(16)):
    print("Already here")
else:
    print("The function doesn't work")
