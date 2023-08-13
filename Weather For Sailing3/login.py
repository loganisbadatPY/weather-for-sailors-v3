# Import necessary libraries
from tkinter import *
from tkinter import ttk
from functools import partial
from PIL import Image, ImageTk
import os
import subprocess
from tkinter import messagebox

# Function to validate user login
def validate_login(username, password):
    user_found = BooleanVar()
    user_found.set(False)

    # Check if either username or password is empty
    if (username.get() == "" or password.get() == ""):
        messagebox.showerror("Error", "Invalid username or password\n\nPlease fill in both username and password fields")
        return

    # Read user data from the users.txt file
    file = open("db/users.txt", "r")
    lines = file.readlines()

    for line in lines:
        user_data = line.strip().split(',')

        line_username = user_data[0]
        line_password = user_data[1]

        if (line_username.strip() == username.get().strip()):
            user_found.set(True)

            if (password.get().strip() == line_password.strip()):
                messagebox.showinfo("Success", "Successfully logged in!")

                # Check if the user has previously set choices
                choices_file = open("db/choices.txt", "r")
                choices_lines = choices_file.readlines()

                user_has_choices = BooleanVar()
                user_has_choices.set(False)

                for choices_line in choices_lines:
                    choices_data = choices_line.split("=")
                    choices_username = choices_data[0]
                    
                    if (choices_username.strip() == username.get().strip()):
                        user_has_choices.set(True)
                        break
                    
                choices_file.close()

                # Save user login in last_user.txt
                user_file = open("last_user.txt", "w")
                user_file.write(username.get().strip())
                user_file.close()

                # Close the current window and redirect based on choices
                tkWindow.destroy()
                if (user_has_choices.get()):
                    import home
                else:
                    import choice_selector
                return
            else:
                messagebox.showerror("Error", "Incorrect password")
                return

    if not (user_found.get()):
        messagebox.showerror("Error", "Username does not exist!")
        return

# Function to handle sign-up button
def sign_up():
    tkWindow.destroy()  # Close the current program
    subprocess.call(["python", "signup.py"])  # Run signup.py

# Create the main tkinter window
tkWindow = Tk()
tkWindow.title('Weather For Sailors')
tkWindow.geometry("700x700")
tkWindow.resizable(width=False, height=False)

# Function to center the window on the screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    width_x = (screen_width - width) // 2
    width_y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{width_x}+{width_y}")

center_window(tkWindow)

# Set up background ocean image
ocean_image = PhotoImage(file="assets/waves_login.png")
ocean_image_label = Label(tkWindow, image=ocean_image)
ocean_image_label.place(x=0, y=0)

# Set up logo image
boat_logo = Image.open("assets/sailing_app_logo.png")
boat_logo = boat_logo.resize((200, 200)) 
boat_logo = ImageTk.PhotoImage(boat_logo)
boat_logo_label = Label(tkWindow, image=boat_logo)
boat_logo_label.place(relx=0.5, rely=0.3, anchor=CENTER)

# Username Label and Text Entry Box
username_label = Label(tkWindow, text="Username:")
username_label.place(relx=0.5, rely=0.48, anchor=CENTER)
username = StringVar()
username_entry = Entry(tkWindow, textvariable=username)
username_entry.place(relx=0.5, rely=0.52, anchor=CENTER)

# Password Label and Text Entry Box
password_label = Label(tkWindow, text="Password:")
password_label.place(relx=0.5, rely=0.57, anchor=CENTER)
password = StringVar()
password_entry = Entry(tkWindow, textvariable=password, show="*")
password_entry.place(relx=0.5, rely=0.61, anchor=CENTER)

# Login Button
validate_login = partial(validate_login, username, password)
login_button = Button(tkWindow, text="Log in", command=validate_login)
login_button.place(relx=0.5, rely=0.65, anchor=CENTER)

# Sign Up Button
sign_up_button = Button(tkWindow, text="Sign Up", command=sign_up)
sign_up_button.place(relx=0.5, rely=0.69, anchor=CENTER)

# Start the tkinter event loop
tkWindow.mainloop()
