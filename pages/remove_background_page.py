import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.font as tkFont
from PIL import Image, ImageTk
from rembg import remove, new_session

FIRST_COLUMN_X = 10
SECOND_COLUMN_X = 200
THIRD_COLUMN_X = 500

FIRST_ROW_Y = 5


class RemoveBackgroundPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        LABEL_FONT = tkFont.Font(family="微软雅黑", size=10, weight="bold")

        self.photo_path = None

        self.photo_frame = ttk.Frame(self)
        self.photo_frame.place(x=FIRST_COLUMN_X, y=FIRST_ROW_Y)

        self.open_photo_button = ttk.Button(
            self.photo_frame, text="打开照片", command=self.open_photo, style="Accent.TButton"
        )
        self.open_photo_button.grid(row=0, column=0)
        self.photo_label = ttk.Label(self.photo_frame, text="照片预览", font=LABEL_FONT)
        self.photo_label.grid(row=1, column=0)

        self.operations_frame = ttk.Frame(self)
        self.operations_frame.place(x=SECOND_COLUMN_X, y=FIRST_ROW_Y)

        self.model_select_label = ttk.Label(self.operations_frame, text="模型选择", font=LABEL_FONT)
        self.model_select_label.grid(row=0, column=0, sticky="w")
        self.model_select_combobox = ttk.Combobox(
            self.operations_frame, width=15, state="readonly"
        )
        self.model_select_combobox["values"] = [
            "silueta",
            "u2net",
            "u2netp",
            "u2net_human_seg",
            "u2net_cloth_seg",
            "isnet-general-use",
            "isnet-anime",
        ]
        self.model_select_combobox.current(0)
        self.model_select_combobox.grid(row=0, column=1, sticky="w")

        self.preview_button = ttk.Button(
            self.operations_frame, text="预览去除背景", command=self.preview, style="Accent.TButton"
        )
        self.preview_button.grid(row=2, column=0, sticky="w")

        self.preview_frame = ttk.Frame(self)
        self.preview_frame.place(x=THIRD_COLUMN_X, y=FIRST_ROW_Y)

        self.preview_label = ttk.Label(self.preview_frame, text="预览", font=LABEL_FONT)
        self.preview_label.grid(row=0, column=0, sticky="w")

    def open_photo(self):
        self.photo_path = filedialog.askopenfilename()
        photo = Image.open(self.photo_path)
        photo_copy = photo.copy()  # 创建照片的副本
        photo_copy.thumbnail((150, 150))  # 调整副本的大小并保持纵横比
        photo_image = ImageTk.PhotoImage(photo_copy, height=150, width=150)
        self.photo_label.config(image=photo_image)
        self.photo_label.image = photo_image  # 保持对图像的引用

    def preview(self):
        # 判断是否选择了照片
        if self.photo_path is None:
            tk.messagebox.showerror("错误", "请先打开照片。")
            return
        photo = Image.open(self.photo_path)
        photo_copy = photo.copy()
        session = new_session(self.model_select_combobox.get())
        photo_removed = remove(photo_copy, session=session)
        photo_removed.thumbnail((300, 300))
        photo_removed_image = ImageTk.PhotoImage(photo_removed)
        self.preview_label.config(image=photo_removed_image)
        self.preview_label.image = photo_removed_image
