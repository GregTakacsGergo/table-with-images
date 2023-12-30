# image_insert_read.py - a program that creates a MySQL database 
# where we can insert, and get images from using a simple navigation menu.
# First insert a picture, so that next you can open it!

import mysql.connector
import os

# MySQL DB connection params
my_db = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "",
	database = "db_with_blob")

# Creating the cursor, and then a MySQL table with a BLOB column containing the images  
my_cursor = my_db.cursor()
my_cursor.execute("CREATE TABLE IF NOT EXISTS Images (image_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, image LONGBLOB NOT NULL, title VARCHAR(20))")

# Defining the function to insert the images into the above created table
def insert_blob(open_file_path):
	with open(open_file_path, 'rb') as file:
		binary_data = file.read()
	SQL_statement = "INSERT INTO Images (image) VALUES (%s)"
	my_cursor.execute(SQL_statement, (binary_data, ))
	my_db.commit()
	inserted_id = my_cursor.lastrowid
	print(f"Image inserted with ID: {inserted_id}")

# Defining image reader, aka fetch function
def fetch_blob(ID):
	SQL_statement2 = "SELECT * FROM Images WHERE image_id = %s"
	my_cursor.execute(SQL_statement2, (str(ID), ))
	my_result = my_cursor.fetchone()[1]
	if my_result is None:
		print(f"No image found with this ID:{ID}")
		return
	if not os.path.exists("image_output"):
		os.makedirs("image_output")
		return
	save_file_path = "image_output/img{0}.jpg".format(str(ID))  # <- here, XY into jpg converter... nvm
	print("Open your destination folder, img{0} should be there!".format(str(ID)))
	with open(save_file_path, 'wb') as file:
		file.write(my_result)

# Navigation menu
def nav_menu():
	print("1.Insert image\n2.Read image")
	menu_input = int(input())
	if menu_input == 1:
		user_file_path = input("Please enter file path:")
		insert_blob(user_file_path)
		print("1.Read image\n2.Exit")
		menu_input_after_insert = int(input())
		if menu_input_after_insert == 1:
			fetch_blob(my_cursor.lastrowid)
		elif menu_input_after_insert == 2:
			print("Bye!")	
			return
	elif menu_input == 2:
		user_ID_choice = input("Please enter image ID:")
		fetch_blob(user_ID_choice)
	else: print("Invalid option, man!")

if __name__ == "__main__":
	try:
		nav_menu()
	except mysql.connector.Error as mysql_err:
		print(f"MySQL Error: {mysql_err}")
	except FileNotFoundError as file_not_found_err:
		print(f"File not found: {file_not_found_err}")
	finally:
		my_db.close()
# -------------------------------------------------------------------------------------------		
# amikor 2.read-et nyomok, lefut, s utána megjelenik a kép
