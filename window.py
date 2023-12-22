import tkinter as tk
from tkinter import filedialog
from lib.id_photo_collage import generate_photo_collage
from PIL import Image, ImageTk


DEFAULT_PHOTO_OPTIONS = [
    {"name": "1寸", "photo_width": 25, "photo_height": 35},
    {"name": "2寸", "photo_width": 35, "photo_height": 50},
]

DEFAULT_PAPER_OPTIONS = [
    {"name": "5寸相纸", "paper_width": 127, "paper_height": 89},
    {"name": "6寸相纸", "paper_width": 152, "paper_height": 102},
    {"name": "A4", "paper_width": 210, "paper_height": 297},
]

FIRST_COLUMN_X = 10
SECOND_COLUMN_X = 150

FIRST_ROW_Y = 5


def open_photo():
    global photo_path
    photo_path = filedialog.askopenfilename()
    photo = Image.open(photo_path)
    photo_copy = photo.copy()  # create a copy of the photo
    photo_copy.thumbnail((150, 150))  # resize the copy while keeping aspect ratio
    photo_image = ImageTk.PhotoImage(photo_copy)
    photo_label.config(image=photo_image)
    photo_label.image = photo_image  # keep a reference to the image


def preview():
    # 判断是否选择了照片
    if photo_path is None:
        tk.messagebox.showerror("Error", "Please open a photo first.")
        return
    # 判断是否输入了照片尺寸
    if photo_width_entry.get() == "" or photo_height_entry.get() == "":
        tk.messagebox.showerror("Error", "Please input photo size.")
        return
    # 判断是否输入了相纸尺寸
    if paper_width_entry.get() == "" or paper_height_entry.get() == "":
        tk.messagebox.showerror("Error", "Please input paper size.")
        return

    photo_size = (int(photo_width_entry.get()), int(photo_height_entry.get()))
    paper_size = (int(paper_width_entry.get()), int(paper_height_entry.get()))
    margin = int(margin_entry.get())
    collage = generate_photo_collage(photo_path, photo_size, paper_size, margin)
    collage.show()


def update_photo_size(*args):
    for option in DEFAULT_PHOTO_OPTIONS:
        if option["name"] == photo_size_var.get():
            photo_width_entry.delete(0, tk.END)
            photo_width_entry.insert(0, option["photo_width"])
            photo_height_entry.delete(0, tk.END)
            photo_height_entry.insert(0, option["photo_height"])


def update_paper_size(*args):
    for option in DEFAULT_PAPER_OPTIONS:
        if option["name"] == paper_size_var.get():
            paper_width_entry.delete(0, tk.END)
            paper_width_entry.insert(0, option["paper_width"])
            paper_height_entry.delete(0, tk.END)
            paper_height_entry.insert(0, option["paper_height"])


root = tk.Tk()
root.geometry("600x400")  # set initial window size to 600x400 pixels
root.title("Photo Collage Generator")

photo_frame = tk.Frame(root)
photo_frame.place(x=FIRST_COLUMN_X, y=FIRST_ROW_Y)

open_photo_button = tk.Button(photo_frame, text="Open Photo", command=open_photo)
open_photo_button.grid(row=0, column=0)
photo_label = tk.Label(photo_frame, text="Photo")
photo_label.grid(row=1, column=0)

photo_size_frame = tk.Frame(root)
photo_size_frame.place(x=SECOND_COLUMN_X, y=FIRST_ROW_Y)

photo_size_label = tk.Label(photo_size_frame, text="Photo Size:", anchor="w")
photo_size_label.grid(row=0, column=0, sticky="w")
photo_size_var = tk.StringVar()
photo_size_var.trace_add("write", update_photo_size)
photo_size_option_menu = tk.OptionMenu(
    photo_size_frame,
    photo_size_var,
    *[option["name"] for option in DEFAULT_PHOTO_OPTIONS]
)
photo_size_option_menu.grid(row=0, column=1, sticky="w")

photo_width_label = tk.Label(photo_size_frame, text="Photo Width(mm):", anchor="w")
photo_width_label.grid(row=1, column=0, sticky="w")
photo_width_entry = tk.Entry(photo_size_frame)
photo_width_entry.grid(row=1, column=1, sticky="w")

photo_height_label = tk.Label(photo_size_frame, text="Photo Height(mm):", anchor="w")
photo_height_label.grid(row=2, column=0, sticky="w")
photo_height_entry = tk.Entry(photo_size_frame)
photo_height_entry.grid(row=2, column=1, sticky="w")

paper_size_frame = tk.Frame(root)
paper_size_frame.place(x=SECOND_COLUMN_X, y=FIRST_ROW_Y + 100)

paper_size_label = tk.Label(paper_size_frame, text="Paper Size:", anchor="w")
paper_size_label.grid(row=0, column=0, sticky="w")
paper_size_var = tk.StringVar()
paper_size_var.trace_add("write", update_paper_size)
paper_size_option_menu = tk.OptionMenu(
    paper_size_frame,
    paper_size_var,
    *[option["name"] for option in DEFAULT_PAPER_OPTIONS]
)
paper_size_option_menu.grid(row=0, column=1, sticky="w")

paper_width_label = tk.Label(paper_size_frame, text="Paper Width(mm):", anchor="w")
paper_width_label.grid(row=1, column=0, sticky="w")
paper_width_entry = tk.Entry(paper_size_frame)
paper_width_entry.grid(row=1, column=1, sticky="w")

paper_height_label = tk.Label(paper_size_frame, text="Paper Height(mm):", anchor="w")
paper_height_label.grid(row=2, column=0, sticky="w")
paper_height_entry = tk.Entry(paper_size_frame)
paper_height_entry.grid(row=2, column=1, sticky="w")

margin_frame = tk.Frame(root)
margin_frame.place(x=SECOND_COLUMN_X, y=FIRST_ROW_Y + 200)

margin_label = tk.Label(margin_frame, text="Margin(mm):", anchor="w")
margin_label.grid(row=0, column=0, sticky="w")
margin_entry = tk.Entry(margin_frame)
margin_entry.grid(row=0, column=1, sticky="w")

operations_frame = tk.Frame(root)
operations_frame.place(x=SECOND_COLUMN_X, y=FIRST_ROW_Y + 250)

preview_button = tk.Button(operations_frame, text="Preview Collage", command=preview)
preview_button.grid(row=0, column=0, sticky="w")

root.mainloop()
