import os
import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.font as tkFont
from PIL import Image, ImageTk
from rembg import remove, new_session
import threading
from pySmartDL import SmartDL
import time


FIRST_COLUMN_X = 0
SECOND_COLUMN_X = 200
THIRD_COLUMN_X = 500

FIRST_ROW_Y = 10

MODELS = [
    {
        "name": "silueta",
        "usage": "人像/自拍",
        "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/silueta.onnx",
        "filename": "silueta.onnx",
    },
    {
        "name": "u2net",
        "usage": "人像/自拍",
        "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx",
        "filename": "u2net.onnx",
    },
    {
        "name": "u2netp",
        "usage": "人像/自拍",
        "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2netp.onnx",
        "filename": "u2netp.onnx",
    },
    {
        "name": "u2net_human_seg",
        "usage": "人像",
        "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx",
        "filename": "u2net_human_seg.onnx",
    },
    {
        "name": "u2net_cloth_seg",
        "usage": "服装",
        "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_cloth_seg.onnx",
        "filename": "u2net_cloth_seg.onnx",
    },
    {
        "name": "isnet-general-use",
        "usage": "通用",
        "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-general-use.onnx",
        "filename": "isnet-general-use.onnx",
    },
    {
        "name": "isnet-anime",
        "usage": "动漫",
        "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-anime.onnx",
        "filename": "isnet-anime.onnx",
    },
]


class RemoveBackgroundPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        LABEL_FONT = tkFont.Font(family="微软雅黑", size=10, weight="bold")

        self.models_path = os.environ.get("U2NET_HOME")

        self.photo_path = None

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

        self.operations_frame = ttk.Frame(self)
        self.operations_frame.place(x=SECOND_COLUMN_X, y=FIRST_ROW_Y)

        self.model_select_label = ttk.Label(
            self.operations_frame, text="模型选择", font=LABEL_FONT
        )
        self.model_select_label.grid(row=0, column=0, sticky="w")
        self.model_select_combobox = ttk.Combobox(
            self.operations_frame, width=15, state="readonly"
        )
        self.model_select_combobox["values"] = [model["name"] for model in MODELS]
        self.model_select_combobox.current(0)
        self.model_select_combobox.bind(
            "<<ComboboxSelected>>", self.update_description_label
        )
        self.model_select_combobox.grid(row=0, column=1, sticky="w")

        self.description_label = ttk.Label(
            self.operations_frame,
            text="用途：" + MODELS[self.model_select_combobox.current()]["usage"],
            font=LABEL_FONT,
        )
        self.description_label.grid(row=1, column=0, sticky="w")

        self.download_model_button = ttk.Button(
            self.operations_frame,
            text="下载模型",
            command=lambda: threading.Thread(
                target=self.download_file,
                args=(
                    MODELS[self.model_select_combobox.current()]["url"],
                    MODELS[self.model_select_combobox.current()]["filename"],
                ),
            ).start(),
            style="Accent.TButton",
        )
        self.download_model_button.grid(row=1, column=1, pady=5, sticky="w")

        self.preview_button = ttk.Button(
            self.operations_frame,
            text="预览去除背景",
            command=self.preview,
            style="Accent.TButton",
        )
        self.preview_button.grid(row=2, column=0, pady=5, sticky="w")

        self.save_button = ttk.Button(
            self.operations_frame,
            text="保存",
            command=self.save,
            style="Accent.TButton",
        )
        self.save_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.preview_frame = ttk.Frame(self)
        self.preview_frame.place(x=THIRD_COLUMN_X, y=FIRST_ROW_Y)

        self.preview_label = ttk.Label(self.preview_frame, text="预览", font=LABEL_FONT)
        self.preview_label.grid(row=0, column=0, padx=150, pady=150, sticky="w")

        self.statusbar = ttk.Label(
            self, text="就绪", border=1, anchor="w", font=LABEL_FONT
        )
        self.statusbar.pack(side="bottom", fill="x")

        self.photo_removed = None

        self.download_in_progress = False

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
        self.photo_removed = remove(photo_copy, session=session)
        photo_removed_copy = self.photo_removed.copy()
        photo_removed_copy.thumbnail((300, 300))
        photo_removed_image = ImageTk.PhotoImage(photo_removed_copy)
        self.preview_label.config(image=photo_removed_image)
        self.preview_label.image = photo_removed_image

    def save(self):
        if self.photo_removed is None:
            tk.messagebox.showerror("错误", "请先预览去除背景。")
            return
        save_path = filedialog.asksaveasfilename(
            defaultextension="png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")],
        )
        self.photo_removed.save(save_path)
        tk.messagebox.showinfo("提示", "保存成功。")

    def download_file(self, url, filename):
        if os.path.exists(os.path.join(self.models_path, filename)):
            tk.messagebox.showinfo("提示", "该模型已下载。")
            return
        if self.download_in_progress:
            tk.messagebox.showinfo("提示", "有模型正在下载中，请稍后。")
            return
        self.download_in_progress = True
        dl = SmartDL(
            [url], dest=os.path.join(self.models_path, filename), progress_bar=False
        )
        dl.start(blocking=False)
        self.statusbar["text"] = "正在下载模型文件：" + filename
        while not dl.isFinished():
            self.statusbar["text"] = (
                "正在下载模型文件："
                + filename
                + "，已下载："
                + "%.2f" % (dl.get_progress() * 100)
                + "%"
            )
            time.sleep(1)
        if dl.isSuccessful():
            self.statusbar["text"] = "下载模型文件：" + filename + "成功。"
        else:
            self.statusbar["text"] = "下载模型文件：" + filename + "失败。"
        self.download_in_progress = False

    def update_description_label(self, event=None):
        # Get the current selection of the combobox
        current_selection = self.model_select_combobox.current()
        # Update the text of the description label
        self.description_label.config(text="用途：" + MODELS[current_selection]["usage"])
