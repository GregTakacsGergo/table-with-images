# In this version I started adding a user interface 

import mysql.connector
import os
import subprocess     # using this module to open file explorer 
from PIL import Image, ImageTk
from tkinter import Tk, Entry, Label, Button, Canvas, PhotoImage, filedialog, simpledialog

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

# Defining a function to get the images from the db into our folder
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
	save_file_path = "image_output/img{0}.jpg".format(str(ID))  
	print("Open your destination folder, img{0} should be there!".format(str(ID)))
	with open(save_file_path, 'wb') as file:
		file.write(my_result)
	
	#display_image(save_file_path)	

# Function to handle the "Insert Image" button
def insert_image():
	try:
	    file_path = filedialog.askopenfilename()
	    if file_path:
	        insert_blob(file_path)
	        print(my_cursor.lastrowid)
	        fetch_blob(my_cursor.lastrowid)
	    	# Create a green check sign image
	        check_image = Image.open("checkmark-16.png")  
	        check_image = check_image.resize((20, 20))
	        check_image_tk = ImageTk.PhotoImage(check_image)
	        # Display the check sign near the "Insert image" button
	        check_label = Label(root, image=check_image_tk)
	        check_label.image = check_image_tk  
	        check_label.grid(row=0, column=1, padx=(10, 0))  
	        success_label.config(text="Image insertion successful")
	        print("Image insertion successful")	       
		    
	except Exception as e:
		x_image = Image.open("x-mark-16.png")
		x_image = x_image.resize((20, 20))
		x_image_tk = ImageTk.PhotoImage(x_image)
		x_label = Label(root, image=x_image_tk)
		x_label.image = x_image_tk
		x_label.grid(row=0, column=1, padx=(10, 0))
		print(f"Image insertion failed. Error: {e}")

# Function to handle the "Read Image" button
def read_image(ID):
	image_id = simpledialog.askinteger("Image ID", "Enter Image ID:")
	if image_id:
		print(image_id)
		fetch_blob(image_id)
		subprocess.run(['explorer', '.'])	
		return

# Function to display image on Tkinter canvas		
def display_image(image_path):
	image = Image.open(image_path)
	img = image.resize((300, 300))
	photo = ImageTk.PhotoImage(img)
	image_label.image = photo    # not finished yet

# Tkinter master window setup
root = Tk()
root.title("Image Viewer")

# Image display canvas
canvas = Canvas(root, width=300, height=300)
canvas.grid()

# Create an Entry widget for image ID input
image_id_entry = Entry(root)

success_label = Label(root, text="")
success_label.grid(row=1, column=0, columnspan=2)

# Tkinter buttons
insert_button = Button(root, text="Insert Image", command=insert_image)
insert_button.grid(row=0, column=0, padx=(0, 10), pady=10)
#insert_button.pack()

read_button = Button(root, text="Read Image", command=lambda:read_image(image_id_entry.get()))
#read_button.pack()

# Tkinter main loop
root.mainloop()

# Cleanup
my_db.close()
# -------------------------------------------------------------------------------------------		
