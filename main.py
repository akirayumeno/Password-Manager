from random import randint, choice
from tkinter import *
from tkinter import messagebox
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password = password_letters + password_numbers + password_symbols

    password = "".join(password)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nWebsite: {website}\n Email/Username: {username} "
                                                      f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    #load the json file
                    data = json.load(data_file)
            except Exception:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # update the json file
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    # save the json file
                    json.dump(data, data_file, indent=4)
            finally:
                # data_file.write(f"{website} | {username} | {password}\n")
                website_entry.delete(0, END)
                username_entry.delete(0, END)
                password_entry.delete(0, END)
# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            # load the json file
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        try:
            username = data[website]["username"]
            password = data[website]["password"]
        except Exception:
            messagebox.showinfo(title="Error", message=f"No details for the {website} exists.")
        else:
            messagebox.showinfo(title=website, message=f"Email/Username: {username}\n Password: {password}")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

#Canva
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

#Label
website_label = Label(text="Website:", fg="black")
website_label.grid(row=1, column=0)
username_label = Label(text="Email/Username:", fg="black")
username_label.grid(row=2, column=0)
password_label = Label(text="Password:", fg="black")
password_label.grid(row=3, column=0)

#Entry
website_entry = Entry(width=18)
website_entry.grid(row=1, column=1)
website_entry.focus()
username_entry = Entry(width=35)
username_entry.grid(row=2, column=1,columnspan=2)
password_entry = Entry(width=18)
password_entry.grid(row=3, column=1)

#Button
generate_button = Button(text="Generate Password", width=13, command=generate_password)
generate_button.grid(row=3, column=2)
add_button = Button(text="Add", width=33, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)
window.mainloop()
