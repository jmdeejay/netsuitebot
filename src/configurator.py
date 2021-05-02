#!/usr/bin/python3

# Standard library imports
import os
import re

# Third party imports
import configparser
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Local application imports
from classes.entry_placeholder import EntryPlaceholder
from classes.entry_time import EntryTime
import classes.logs as logs
import classes.tasks as tasks
import classes.utilities as utilities
from netsuitebot import try_login

# Consts
VERSION = "1.0"
TITLE = "NetsuiteBot configurator"
CONFIG_FILE = "configs.ini"


def popup(title, value, timeout=0):
    popup_root = tk.Toplevel()
    popup_root.wm_title(title)
    popup_root.rowconfigure(1, minsize=50, weight=1)
    popup_root.columnconfigure(0, minsize=300, weight=1)
    if timeout > 0:
        popup_root.after(timeout, popup_root.destroy)

    label = tk.Label(popup_root, text=value, padx=10, pady=5)
    label.grid(row=0, column=0)
    popup_button = tk.Button(popup_root, text="Ok", command=popup_root.destroy)
    popup_button.grid(row=1, column=0)


def write_config_file():
    config.write(open(CONFIG_FILE, "w"))


def open_config_file():
    if not os.path.exists(CONFIG_FILE):
        config["Credentials"] = {"Email": "", "Password": ""}
        config["Informations"] = {
            "Task": tasks.get_default_task(),
            "Time": "7:30",
            "Comment": "Standup, analyse, développement"
        }
        write_config_file()
    else:
        config.read(CONFIG_FILE)

    try:
        edit_email.insert(tk.END, utilities.decode_base64(config.get("Credentials", "Email")))
        edit_password.insert(tk.END, utilities.secure_decode_base64(config.get("Credentials", "Password")))

        task_id = config.get("Informations", "Task")
        if not tasks.is_valid_task_id(task_id):
            task_id = tasks.get_default_task()
        combo_task.current(tasks.get_task_index_by_id(task_id))
        edit_time.insert(tk.END, config.get("Informations", "Time"))
        edit_comment.insert(tk.END, config.get("Informations", "Comment"))
    except configparser.NoOptionError:
        logs.log_error("Ini file corrupted. Try deleting the " + CONFIG_FILE + " file.")
    except UnicodeDecodeError:
        logs.log_error("Error decoding data. Try recreating the " + CONFIG_FILE + " file.")
    except utilities.binascii.Error:
        logs.log_error("Error decoding data. Try recreating the " + CONFIG_FILE + " file.")


def save_config_file():
    if edit_email.get() == "" or edit_password.get() == "":
        popup("Info", "Email/Password cannot be empty.", 2000)
    elif edit_time.get() == "":
        popup("Info", "Time cannot be empty.", 2000)
    elif not utilities.valid_time(edit_time.get()):
        popup("Info", "Time must be in a valid format (7:30).", 2000)
    elif edit_comment.get().strip() == "":
        popup("Info", "Comment cannot be empty.", 2000)
    else:
        config.set("Credentials", "Email", utilities.encode_base64(edit_email.get()))
        config.set("Credentials", "Password", utilities.secure_encode_base64(edit_password.get()))

        config.set("Informations", "Task", str(tasks.get_task_id_by_index(combo_task.current())))
        config.set("Informations", "Time", edit_time.get())
        config.set("Informations", "Comment", edit_comment.get())
        write_config_file()
        popup("Info", "NetsuiteBot configurations updated successfully.", 2000)


def test_login():
    login_result = try_login(edit_email.get(), edit_password.get())
    if login_result is not None:
        label_status.configure(text="Success", fg="green")
        popup("Info", "Authentication successful!")
    else:
        label_status.configure(text="Error", fg="red")
        popup("Error", "Incorrect email or password.")


def load_image(filepath, width=0, height=0):
    full_path = utilities.resource_path(filepath)
    if os.path.exists(full_path):
        image = Image.open(full_path)
        if width > 0 and height > 0:
            image = image.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)
    return None


def format_time_inputs(time_text):
    time_text.set(re.sub(r"[^0-9:.]", "", time_text.get()))
    if len(edit_time.get()) > 5:
        time_text.set(edit_time.get()[:-1])


if __name__ == "__main__":
    config = configparser.ConfigParser()

    window = tk.Tk()
    window.title(TITLE)
    window.resizable(False, False)

    frame_login = ttk.Frame(window)
    frame_login.grid(row=0, column=0, sticky="new", padx=10)
    frame_login.rowconfigure(0, minsize=35)
    frame_login.rowconfigure(1, minsize=35)
    frame_login.columnconfigure(0, minsize=50)
    frame_login.columnconfigure(1, minsize=250, weight=2)
    frame_login.columnconfigure(2, minsize=50)

    label_email = ttk.Label(frame_login, text="Email:")
    label_password = ttk.Label(frame_login, text="Password:")
    edit_email = EntryPlaceholder(frame_login, "email@example.com")
    edit_password = ttk.Entry(frame_login, show="*")
    label_status = tk.Label(frame_login, width=10, justify="center", anchor="center", font="none 12 bold")
    btn_test_login = ttk.Button(frame_login, text="Test login", command=test_login)

    label_email.grid(row=0, column=0, sticky="nw", pady=6)
    label_password.grid(row=1, column=0, sticky="nw", pady=6)
    edit_email.grid(row=0, column=1, sticky="ew", padx=10)
    edit_password.grid(row=1, column=1, sticky="ew", padx=10)
    label_status.grid(row=0, column=2, sticky="nw", pady=6)
    btn_test_login.grid(row=1, column=2, sticky="ew")

    # ===============================

    separator = ttk.Separator(window)
    separator.grid(row=1, column=0, sticky="ew", padx=10, pady=2)

    # ===============================

    frame_infos = ttk.Frame(window)
    frame_infos.grid(row=2, column=0, sticky="nsew", padx=10)
    frame_infos.rowconfigure(0, minsize=10)
    frame_infos.rowconfigure(1, minsize=35)
    frame_infos.columnconfigure(0, minsize=70)
    frame_infos.columnconfigure(1, minsize=30)
    frame_infos.columnconfigure(2, minsize=250, weight=2)

    label_task = ttk.Label(frame_infos, text="Task:")
    label_time = ttk.Label(frame_infos, text="Time:")
    label_comment = ttk.Label(frame_infos, text="Comment:")

    combo_task = ttk.Combobox(frame_infos, state="readonly", width=15, values=tasks.get_tasks_values())
    combo_task.current(0)

    time_value = tk.StringVar()
    edit_time = EntryTime(frame_infos, textvariable=time_value, width=5)
    time_value.trace("w", lambda *args: format_time_inputs(time_value))
    edit_comment = ttk.Entry(frame_infos)

    label_task.grid(row=0, column=0, sticky="nw")
    label_time.grid(row=0, column=1, sticky="nw", padx=10)
    label_comment.grid(row=0, column=2, sticky="nw")
    combo_task.grid(row=1, column=0, sticky="ew")
    edit_time.grid(row=1, column=1, sticky="w", padx=10)
    edit_comment.grid(row=1, column=2, sticky="ew")

    # ===============================

    separator = ttk.Separator(window)
    separator.grid(row=3, column=0, sticky="ew", padx=10, pady=2)

    # ===============================

    frame_bottom = ttk.Frame(window)
    frame_bottom.grid(row=4, column=0, sticky="nsew", padx=10)
    frame_bottom.rowconfigure(0, minsize=35, weight=1)
    frame_bottom.columnconfigure(0, minsize=150, weight=1)
    frame_bottom.columnconfigure(1, minsize=150, weight=2)
    frame_bottom.columnconfigure(2, minsize=50)

    image_netsuite = load_image("src/netsuite_logo.png", 260, 40)
    label_netsuite_img = tk.Label(frame_bottom, image=image_netsuite)
    label_netsuite_img.place(x=0, y=0)
    label_netsuite_img.grid(row=0, column=0, sticky="sw")

    label_version = ttk.Label(frame_bottom, text="v." + VERSION)
    label_version.grid(row=0, column=1, sticky="sw")
    btn_save = ttk.Button(frame_bottom, text="Save configs", command=save_config_file)
    btn_save.grid(row=0, column=2, sticky="ew")

    open_config_file()
    window.mainloop()
