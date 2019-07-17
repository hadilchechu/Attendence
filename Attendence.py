#!/usr/bin/env python3

import os
import os.path
import sys
import sqlite3 as sql
import subprocess
from datetime import datetime, date, time

# Make sqlite3 database connection
DB_NAME = 'att.db'
conn = sql.connect(DB_NAME)
cursor = conn.cursor()

# Header
header = """

   ██████  ██████ ██████ ████ █▀▄  █  █████▄
  ▓██  ██▒▓   █ ▀ ▀  █ ▒ █    █ ▓  █  ██   █   
  ▓██  ██ ▒▒  █      █   █    █ ▓  █  ██   █▒ 
  ▒██▀▀██  ▒  █ ▀    █ ▒ █▀▀  █  █ █  ██   █  ▒  
  ▓██  ██ ▒▒  █      █   █ ▒  █ ░█ █ ▓██▒  █ ▒░
  ░██  ██ ▒░▒▒█▒▒░░  █▒  ████ █ ▒░██ ░█████▀░ 
  ░ ▒  ░▒▓░░░ ▒░ █░▒░   ░  ░░▓  ░ ▒░   ▒ ▒  ▒▒▓  ▒ 
  ░▒ ░ ▒░ ░ ░  ░░  ░      ░ ▒ ░░ ░░   ░ ▒░ ░ ▒  ▒ 
  ░░   ░    ░   █      ░    ▒ ░   ░   ░ ░  ░ ░  ░ 
   ░        ░  ░       ░    ░           ░    ░                                                                  
"""

menu = """

 	CREATE		UPDATE		DELETE		VIEW		SORT	 	 EXIT
 	press 0		press 1		press 2		press 3		press 4		 press 5 



		"""

		
# If a table donot exist then, creates a table and if exist then wont overwrite
def create_table():
	cursor.executescript("""
		CREATE TABLE IF NOT EXISTS attend (
    	Roll_NO  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    	Name    TEXT,
		create_date TEXT);
		""")

# Function for data insertion 
def insert_data(rem_name):
	cursor.execute('''INSERT OR IGNORE INTO attend (
		Name, create_date) 
        VALUES ( ?, ? )''', ( rem_name, str(datetime.now()).split('.')[0])) 
	conn.commit()
	main_menu()
# data creation function
def create_data():
	os.system('clear')
	data_content = input('Name of the student? ')
	

	# Joined date and time 

	print("Joined at",str(datetime.now()))
	insert_data(data_content)
	main_menu()

#For viewing the whole list
def view_data(rec=0):
	if rec == 0:
		os.system('clear')
		cursor.execute("SELECT *FROM attend")
		data = cursor.fetchall()
		print("{0:5} {1:20} {2:25} ".format("|Roll_NO|", "  |Name|", "|created date     |"))
		print("{0:5} {1:20} {2:25} ".format("-"*8, "-"*7, "-"*19))
		for item in data:
			print("{0:10} {1:25} {2:25} ".format(str(item[0]), item[1], item[2]))
		
	else:
		os.system('clear')
		cursor.execute("DELETE FROM attend WHERE Roll_NO = ?", (rec, ))
		conn.commit()

		cursor.execute("SELECT *FROM attend")
		data = cursor.fetchall()
		
		print("{0:5} {1:20} {2:25}".format("|Roll_NO|", "|  Name|", "|created date|"))
		print("{0:5} {1:20} {2:25} ".format("-"*8, "-"*7, "-"*19))
		for item in data:
			print("{0:10} {1:20} {2:25} ".format(item[0], item[1], item[2]))
		main_menu()

# Sort Date by descending order
def sort_date_d():
		os.system('clear')
		cursor.execute("SELECT * FROM attend ORDER BY create_date DESC")		
		data = cursor.fetchall()
		print("{0:5} {1:20} {2:25} ".format("|Roll_NO|", "|  Name|", "|created date     |"))
		print("{0:5} {1:20} {2:25} ".format("-"*8, "-"*7, "-"*19))
		for item in data:
			print("{0:10} {1:20} {2:25} ".format(str(item[0]), item[1], item[2]))
		main_menu()

# Sort Date by ascending order		
def sort_date_a():
		os.system('clear')
		cursor.execute("SELECT * FROM attend ORDER BY create_date ASC")		
		data = cursor.fetchall()
		print("{0:5} {1:20} {2:25} ".format("|Roll_NO|", "  |Name|", "|created date     |"))
		print("{0:5} {1:20} {2:25} ".format("-"*8, "-"*7, "-"*19))
		for item in data:
			print("{0:10} {1:20} {2:25} ".format(str(item[0]), item[1], item[2]))
		main_menu()

#Choose whether the data is ascending or descending
def choose():
	print("1.DESCENDING order by Date  \n2.ASCENDING order by Date ")
	c= input(">>> ")

	if int(c) == 1:
	
		sort_date_d()
	
	if int(c) == 2:
	
		sort_date_a()
	main_menu()

# Updation of TASKS already exist
def update_data():
	#os.system('clear')

	task_Roll_NO = input(" Which data you want to Update? (Roll_NO) ")
	if int(task_Roll_NO) == -99:
		main_menu()
	view_data()
	print("\n{0:~^20s}".format("Update section"))
	data_content = input('What you want to add? ')
	

	cursor.execute('''UPDATE attend 
					SET Name = ?,
					create_date = ?
					WHERE Roll_NO =?''',
					(data_content, 
						str(datetime.now()).split('.')[0],
						task_Roll_NO)) 
	conn.commit()
	main_menu()
# Dict of CLI menu_items
menuItems = [
    { "Create data": 0 },
    { "Update data": 1 },
	{ "Delete specific": 2 },
    { "View all": 3 },
    { "Sort": 4 },
	{ "Exit": 5 },
]


#Main menu			
def main_menu():                                
	while True:
		#os.system('clear')
		print(header,"\n")
		print(menu,"\n")

		choice = input(">>> ")
		try:
			if int(choice) < 0: pass
			elif int(choice) == 0:
				create_data()

			elif int(choice) == 1:
				update_data()

			elif int(choice) == 2:
				view_data(0)
				view_data(input("What you want to Update ? ENTER Roll_NO"))

			elif int(choice) == 3:
				view_data(0)
				main_menu()

			elif int(choice) == 4:
				choose()

			elif int(choice) == 5:
				sys.exit(0)
			else:
				pass
		except ValueError:
			print("InvalRoll_NO option")
			os.system('clear')
		except IndexError:
			print("Out of index")
			os.system('clear')

if __name__ == '__main__':
	
	create_table()
	main_menu()
