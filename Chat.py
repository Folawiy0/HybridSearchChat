import os
from xvfbwrapper import Xvfb
import tkinter as tk
from tkinter import ttk

class LangChainDeprecationWarning(UserWarning):
    pass

import warnings
warnings.simplefilter("ignore", LangChainDeprecationWarning)

xvfb = Xvfb(width=1280, height=720)
xvfb.start()

os.environ['DISPLAY'] = ':99'

def process_and_display_response():
    query = entry.get()
    response = "Response: This is just a placeholder response for the query: " + query
    text.insert(tk.END, response + "\n")
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("HYBRID Chat")

entry = ttk.Entry(root, font=("Arial", 14))
entry.pack(padx=20, pady=20, fill=tk.X)

ask_button = ttk.Button(root, text="Ask", command=process_and_display_response)
ask_button.pack(padx=20, pady=5)

text = tk.Text(root, height=10, width=60, font=("Arial", 14))
text.pack(padx=20, pady=20)

exit_button = ttk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(padx=20, pady=5)

root.mainloop()
