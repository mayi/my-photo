import base64
import os
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from PIL import Image
from pySmartDL import SmartDL
import time
from rembg import remove, new_session
import threading
from lib.queue import TimePriorityQueue


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


class RemoveBackgroundPage:
    def __init__(self):
        self.download_in_progress = False
        self.models_path = os.environ.get("U2NET_HOME")
        self.model = MODELS[0]
        self.photo_path = None
        self.photo = None
        self.queue = TimePriorityQueue(
            name="remove_background",
            namespace="myphoto",
            host="localhost",
            port=6379,
            db=0,
        )
        # 新线程中处理清除队列中超时的任务
        threading.Thread(target=self.clean_queue, daemon=True).start()
        self.create_widgets()

    def download_file(self, url, filename):
        if os.path.exists(os.path.join(self.models_path, filename)):
            st.toast("模型已存在，无需下载")
            return
        if self.download_in_progress:
            st.toast("有模型正在下载中，请稍后再试")
            return
        self.download_in_progress = True
        dl = SmartDL(
            [url], dest=os.path.join(self.models_path, filename), progress_bar=False
        )
        dl.start(blocking=False)

        progress_bar = st.progress(0)

        while not dl.isFinished():
            progress = dl.get_progress()
            progress_bar.progress(progress)
            time.sleep(1)
        if dl.isSuccessful():
            st.toast("模型下载成功")
            progress_bar.empty()
        else:
            st.toast("模型下载失败")
            progress_bar.empty()
        self.download_in_progress = False

    def preview(self):
        if self.photo is None:
            st.toast("请先上传图片")
            return
        key = generate_request_key(self.model["name"], self.photo_path)
        self.queue.enqueue(key)

        while self.queue.peek() != key:
            index = self.queue.index(key)
            with st.spinner(f"您的任务在队列中排在第{index+1}位，请稍候......"):
                time.sleep(2)
        with st.spinner("正在处理图片..."):
            session = new_session(self.model["name"])
            photo_copy = self.photo.copy()
            removed = remove(photo_copy, session=session)
            self.queue.remove(key)
            st.subheader("预览")
            preview_container = st.container(border=True)
            preview_container.image(removed, width=300)
            preview_container.write("右键点击图片，选择“另存为”保存图片。")

    def create_widgets(self):
        st.title("去除图片背景")
        st.subheader("选择模型")
        model_container = st.container(border=True)
        selected_model = model_container.selectbox(
            "选择模型", [model["name"] for model in MODELS]
        )
        # descript the model
        self.model = next(model for model in MODELS if model["name"] == selected_model)
        model_container.write(f"用途：{self.model['usage']}")
        # download button
        download_button = model_container.button(
            "下载", type="secondary", disabled=self.download_in_progress
        )
        if download_button:
            self.download_file(self.model["url"], self.model["filename"])
        st.subheader("上传图片")
        photo_container = st.container(border=True)
        self.photo_path = photo_container.file_uploader(
            "上传照片", type=["jpg", "png", "jpeg"]
        )
        if self.photo_path is not None:
            self.photo = Image.open(self.photo_path)
            photo_container.image(image=self.photo, width=100)
        preview_button = st.button("预览", type="primary")
        if preview_button:
            self.preview()

    # 定期清理队列中存在超过2分钟的任务
    def clean_queue(self):
        while True:
            self.queue.clean(time.time() - 120)
            time.sleep(60)

def get_session_id():
    ctx = get_script_run_ctx()
    session_id = ctx.session_id
    return session_id


def generate_request_key(model_name, photo_path):
    # 获得SessionId+模型名+图片路径的唯一标识，Base64编码，使用该标识作为redis队列的key，避免重复提交，同时也可以用于查询任务状态
    session_id = get_session_id()
    key = f"{session_id}_{model_name}_{photo_path}"
    # BASE64编码
    key = base64.b64encode(key.encode()).decode()
    return key


if __name__ == "__main__":
    RemoveBackgroundPage()
