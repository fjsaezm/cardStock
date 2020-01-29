import os
import csv
import datetime
import pprint
from prettytable import from_db_cursor
import sqlite3

connection = sqlite3.connect("stock.db")
cursor = connection.cursor()


def init_database():
    sql_create = """CREATE TABLE IF NOT EXISTS purchases (
purchase INTEGER PRIMARY KEY AUTOINCREMENT,
copies INT NOT NULL,
cardname VARCHAR(30),
total_price DOUBLE,
date DATE ); """
    cursor.execute(sql_create)
    sql_create = """CREATE TABLE IF NOT EXISTS sellings (
selling INTEGER PRIMARY KEY AUTOINCREMENT,
copies INT NOT NULL,
cardname VARCHAR(30),
total_price DOUBLE,
date DATE); """
    cursor.execute(sql_create)
    save_changes()

def reset_database():
    cursor.execute('drop table if exists purchases')
    cursor.execute('drop table if exists sellings')
    init_database()


def append_purchase(cardname,copies,totalprice):
    sql_command = """INSERT INTO purchases (copies,cardname,total_price,date) VALUES ("{first}","{second}","{third}","{forth}")
    """
    date = str(datetime.date.today())
    sql_command = sql_command.format(first = copies,second = cardname,third = totalprice,forth = date)
    cursor.execute(sql_command)
    save_changes()

def del_purchase(num):
    cursor.execute("delete from purchases where purchase = {}".format(num))
    

def clear_table(table):
    cursor.execute('drop table if exists %s',table)
    init_database()


def show_purchases():
    cursor.execute("SELECT * FROM purchases")
    x = from_db_cursor(cursor)
    print(x)

def save_changes():
    connection.commit()

def save_and_exit():
    connection.commit()
    connection.close()

def ask_for_purchase():
    cardname = input("What card did you buy? ")
    copies   = input("How many copies did you buy? ")
    totalprice = input("How much did it ALL cost? ")
    append_purchase(cardname,copies,totalprice)

def ask_for_delete_purchase():
    num = input("What number of purchase do you want to delete? ")
    if int(num) > 0:
        del_purchase(num)


#reset_database()
init_database()
ask_for_purchase()
ask_for_delete_purchase()
show_purchases()
save_and_exit()



