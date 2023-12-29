import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.font as tkFont
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

FIRST_COLUMN_X = 0
SECOND_COLUMN_X = 200
THIRD_COLUMN_X = 500

FIRST_ROW_Y = 10


class CollagePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        LABEL_FONT = tkFont.Font(family="微软雅黑", size=10, weight="bold")

        self.photo_path = None

        validate_command = self.register(self.is_positive_integer)

        self.photo_frame = ttk.Frame(self)
        self.photo_frame.place(x=FIRST_COLUMN_X, y=FIRST_ROW_Y)

        self.open_photo_button = ttk.Button(
            self.photo_frame,
            text="打开照片",
            command=self.open_photo,
            style="Accent.TButton",
        )
        self.open_photo_button.grid(row=0, column=0, padx=50)
        self.photo_label = ttk.Label(self.photo_frame, text="照片预览", font=LABEL_FONT)
        self.photo_label.grid(row=1, column=0, pady=75)

        self.photo_size_frame = ttk.Frame(self)
        self.photo_size_frame.place(x=SECOND_COLUMN_X, y=FIRST_ROW_Y)

        self.photo_size_label = ttk.Label(
            self.photo_size_frame, text="照片尺寸:", anchor="w", font=LABEL_FONT
        )
        self.photo_size_label.grid(row=0, column=0, sticky="w")

        self.photo_size_combobox = ttk.Combobox(
            self.photo_size_frame, width=15, state="readonly"
        )
        self.photo_size_combobox["values"] = [
            option["name"] for option in DEFAULT_PHOTO_OPTIONS
        ]
        self.photo_size_combobox.current(0)
        self.photo_size_combobox.bind("<<ComboboxSelected>>", self.update_photo_size)
        self.photo_size_combobox.grid(row=0, column=1, sticky="w")

        self.photo_width_label = ttk.Label(
            self.photo_size_frame, text="照片宽度(mm):", anchor="w", font=LABEL_FONT
        )
        self.photo_width_label.grid(row=1, column=0, sticky="w")
        self.photo_width_entry = ttk.Entry(
            self.photo_size_frame,
            validate="key",
            validatecommand=(validate_command, "%P"),
        )
        self.photo_width_entry.insert(0, 25)
        self.photo_width_entry.grid(row=1, column=1, sticky="w")

        self.photo_height_label = ttk.Label(
            self.photo_size_frame, text="照片高度(mm):", anchor="w", font=LABEL_FONT
        )
        self.photo_height_label.grid(row=2, column=0, sticky="w")
        self.photo_height_entry = ttk.Entry(
            self.photo_size_frame,
            validate="key",
            validatecommand=(validate_command, "%P"),
        )
        self.photo_height_entry.insert(0, 35)
        self.photo_height_entry.grid(row=2, column=1, sticky="w")

        self.paper_size_frame = ttk.Frame(self)
        self.paper_size_frame.place(x=SECOND_COLUMN_X, y=FIRST_ROW_Y + 100)

        self.paper_size_label = ttk.Label(
            self.paper_size_frame, text="相纸尺寸:", anchor="w", font=LABEL_FONT
        )
        self.paper_size_label.grid(row=0, column=0, sticky="w")

        self.paper_size_combobox = ttk.Combobox(
            self.paper_size_frame, width=15, state="readonly"
        )
        self.paper_size_combobox["values"] = [
            option["name"] for option in DEFAULT_PAPER_OPTIONS
        ]
        self.paper_size_combobox.current(0)
        self.paper_size_combobox.bind("<<ComboboxSelected>>", self.update_paper_size)
        self.paper_size_combobox.grid(row=0, column=1, sticky="w")

        self.paper_width_label = ttk.Label(
            self.paper_size_frame, text="相纸宽度(mm):", anchor="w", font=LABEL_FONT
        )
        self.paper_width_label.grid(row=1, column=0, sticky="w")
        self.paper_width_entry = ttk.Entry(
            self.paper_size_frame,
            validate="key",
            validatecommand=(validate_command, "%P"),
        )
        self.paper_width_entry.insert(0, 127)
        self.paper_width_entry.grid(row=1, column=1, sticky="w")

        self.paper_height_label = ttk.Label(
            self.paper_size_frame, text="相纸高度(mm):", anchor="w", font=LABEL_FONT
        )
        self.paper_height_label.grid(row=2, column=0, sticky="w")
        self.paper_height_entry = ttk.Entry(
            self.paper_size_frame,
            validate="key",
            validatecommand=(validate_command, "%P"),
        )
        self.paper_height_entry.insert(0, 89)
        self.paper_height_entry.grid(row=2, column=1, sticky="w")

        self.margin_frame = ttk.Frame(self)
        self.margin_frame.place(x=SECOND_COLUMN_X, y=FIRST_ROW_Y + 200)

        self.margin_label = ttk.Label(
            self.margin_frame, text="边距(mm):", anchor="w", font=LABEL_FONT
        )
        self.margin_label.grid(row=0, column=0, sticky="w")
        self.margin_entry = ttk.Entry(
            self.margin_frame, validate="key", validatecommand=(validate_command, "%P")
        )
        self.margin_entry.insert(0, 10)
        self.margin_entry.grid(row=0, column=1, sticky="w")

        self.operations_frame = ttk.Frame(self)
        self.operations_frame.place(x=SECOND_COLUMN_X, y=FIRST_ROW_Y + 250)

        self.preview_button = ttk.Button(
            self.operations_frame,
            text="预览拼贴",
            command=self.preview,
            style="Accent.TButton",
        )
        self.preview_button.grid(row=0, column=0, sticky="w")

        self.save_button = ttk.Button(
            self.operations_frame,
            text="保存拼贴",
            command=self.save,
            style="Accent.TButton",
        )
        self.save_button.grid(row=0, column=1, padx=5, sticky="w")

        self.preview_frame = ttk.Frame(self)
        self.preview_frame.place(x=THIRD_COLUMN_X, y=FIRST_ROW_Y)

        self.preview_label = ttk.Label(self.preview_frame, text="预览", font=LABEL_FONT)
        self.preview_label.grid(row=0, column=0, padx=150, pady=150, sticky="w")

        self.collage = None

    def open_photo(self):
        self.photo_path = filedialog.askopenfilename()
        photo = Image.open(self.photo_path)
        photo_copy = photo.copy()  # 创建照片的副本
        photo_copy.thumbnail((150, 150))  # 调整副本的大小并保持纵横比
        photo_image = ImageTk.PhotoImage(photo_copy)
        self.photo_label.config(image=photo_image)
        self.photo_label.image = photo_image  # 保持对图像的引用

    def preview(self):
        # 判断是否选择了照片
        if self.photo_path is None:
            tk.messagebox.showerror("错误", "请先打开照片。")
            return
        # 判断是否输入了照片尺寸
        if self.photo_width_entry.get() == "" or self.photo_height_entry.get() == "":
            ttk.messagebox.showerror("错误", "请输入照片尺寸。")
            return
        # 判断是否输入了相纸尺寸
        if self.paper_width_entry.get() == "" or self.paper_height_entry.get() == "":
            tk.messagebox.showerror("错误", "请输入相纸尺寸。")
            return
        # 判断是否输入了边距
        if self.margin_entry.get() == "":
            tk.messagebox.showerror("错误", "请输入边距。")
            return
        photo_size = (
            int(self.photo_width_entry.get()),
            int(self.photo_height_entry.get()),
        )
        paper_size = (
            int(self.paper_width_entry.get()),
            int(self.paper_height_entry.get()),
        )
        margin = int(self.margin_entry.get())
        self.collage = generate_photo_collage(
            self.photo_path, photo_size, paper_size, margin
        )
        collage_copy = self.collage.copy()
        collage_copy.thumbnail((300, 300))
        collage_image = ImageTk.PhotoImage(collage_copy)
        self.preview_label.config(image=collage_image)
        self.preview_label.image = collage_image

    def save(self):
        if self.collage is None:
            tk.messagebox.showerror("错误", "请先预览拼贴。")
            return
        save_path = filedialog.asksaveasfilename(
            defaultextension="jpg", filetypes=[("JPEG", "*.jpg")]
        )
        self.collage.save(save_path)
        tk.messagebox.showinfo("提示", "保存成功。")

    def update_photo_size(self, event):
        for option in DEFAULT_PHOTO_OPTIONS:
            if option["name"] == event.widget.get():
                self.photo_width_entry.delete(0, tk.END)
                self.photo_width_entry.insert(0, option["photo_width"])
                self.photo_height_entry.delete(0, tk.END)
                self.photo_height_entry.insert(0, option["photo_height"])

    def update_paper_size(self, event):
        for option in DEFAULT_PAPER_OPTIONS:
            if option["name"] == event.widget.get():
                self.paper_width_entry.delete(0, tk.END)
                self.paper_width_entry.insert(0, option["paper_width"])
                self.paper_height_entry.delete(0, tk.END)
                self.paper_height_entry.insert(0, option["paper_height"])

    def is_positive_integer(self, s):
        if s == "":
            return True
        return s.isdigit()
