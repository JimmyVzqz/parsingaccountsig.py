# import json

# # Load the followers file (list of objects)
# with open("followers_1.json", "r", encoding="utf-8") as f:
#     followers_data = json.load(f)

# # Load the following file (dict with key relationships_following)
# with open("following.json", "r", encoding="utf-8") as f:
#     following_data = json.load(f)["relationships_following"]

# # Extract usernames from each file
# followers_usrset = set(
#     item["string_list_data"][0]["value"]
#     for item in followers_data
#     if item["string_list_data"]
# )

# following_usrset = set(
#     item["string_list_data"][0]["value"]
#     for item in following_data
#     if item["string_list_data"]
# )

# # Calculate users you follow who do not follow you back
# not_following_back = following_usrset - followers_usrset

# # Output the results
# print("Accounts you follow that don't follow you back:")
# for user in sorted(not_following_back):
#     print(user)

# Adding GUI and unzip process:

import json
import zipfile
import os
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox

def process_instagram_zip():
    # Open file dialog to select ZIP file
    zip_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
    if not zip_path:
        return

    # Create a temporary directory to extract files
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        except zipfile.BadZipFile:
            messagebox.showerror("Error", "Selected file is not a valid ZIP.")
            return

        # Locate the required JSON files
        followers_file = None
        following_file = None

        for dirpath, dirs, files in os.walk(temp_dir):
            for file in files:
                if "followers_1" in file.lower() and file.endswith(".json"):
                    followers_file = os.path.join(dirpath, file)
                elif "following" in file.lower() and file.endswith(".json"):
                    following_file = os.path.join(dirpath, file)

        if not followers_file or not following_file:
            messagebox.showerror("Error", "Could not find both followers and following JSON files.")
            return

        # Load followers
        with open(followers_file, "r", encoding="utf-8") as f:
            followers_data = json.load(f)

        followers = set(
            item["string_list_data"][0]["value"]
            for item in followers_data
            if item.get("string_list_data")
        )

        # Load following
        with open(following_file, "r", encoding="utf-8") as f:
            following_data = json.load(f)["relationships_following"]

        following = set(
            item["string_list_data"][0]["value"]
            for item in following_data
            if item.get("string_list_data")
        )

        not_following_back = sorted(following - followers)

        if not not_following_back:
            messagebox.showinfo("Done", "Everyone you follow follows you back!")
            return

        # Show results in a new window
        result_window = tk.Toplevel(root)
        result_window.title("Not Following Back")

        text = tk.Text(result_window, wrap="word", height=30, width=50)
        text.pack(padx=10, pady=10)

        for user in not_following_back:
            text.insert(tk.END, user + "\n")

        text.config(state=tk.DISABLED)

# Set up GUI
root = tk.Tk()
root.title("Instagram Follower Checker")
root.geometry("300x150")

label = tk.Label(root, text="Select your Instagram ZIP file:")
label.pack(pady=10)

button = tk.Button(root, text="Choose File", command=process_instagram_zip)
button.pack(pady=5)

root.mainloop()

