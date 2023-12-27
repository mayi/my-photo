import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import sv_ttk
from pages.collage_page import CollagePage
from pages.remove_background_page import RemoveBackgroundPage

root = tk.Tk()
root.geometry("800x400")
root.title("照片处理器")

notebook = ttk.Notebook(root)

collage_page = CollagePage(notebook)

notebook.add(collage_page, text="照片拼贴")

remove_background_page = RemoveBackgroundPage(notebook)

notebook.add(remove_background_page, text="去除背景")

notebook.pack(expand=True, fill="both")

sv_ttk.use_light_theme()

root.mainloop()
