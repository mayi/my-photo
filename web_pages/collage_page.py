import streamlit as st
from PIL import Image

from lib.id_photo_collage import generate_photo_collage

DEFAULT_PHOTO_OPTIONS = [
    {"name": "1寸", "photo_width": 25, "photo_height": 35},
    {"name": "2寸", "photo_width": 35, "photo_height": 50},
    {"name": "自定义", "photo_width": 25, "photo_height": 35},
]

DEFAULT_PAPER_OPTIONS = [
    {"name": "5寸相纸", "paper_width": 127, "paper_height": 89},
    {"name": "6寸相纸", "paper_width": 152, "paper_height": 102},
    {"name": "A4", "paper_width": 210, "paper_height": 297},
    {"name": "A3", "paper_width": 297, "paper_height": 420},
    {"name": "自定义", "paper_width": 127, "paper_height": 89},
]


def main():
    st.title("照片处理器")
    st.subheader("照片拼贴")
    photo_container = st.container(border=True)
    photo_file = photo_container.file_uploader("上传照片", type=["jpg", "png", "jpeg"])
    if photo_file is not None:
        photo = Image.open(photo_file)
        photo_container.image(image=photo, width=100)
    col1, col2 = st.columns(2)
    with col1:
        photo_size_container = st.container(border=True)
        photo_size_container.write("照片尺寸(单位：毫米)")
        selected_photo_option = photo_size_container.selectbox(
            "选择照片尺寸", [option["name"] for option in DEFAULT_PHOTO_OPTIONS]
        )
        if selected_photo_option == "自定义":
            photo_width = photo_size_container.number_input("宽度", min_value=1, value=25)
            photo_height = photo_size_container.number_input("高度", min_value=1, value=35)
        else:
            # Find the selected option
            selected_option = next(option for option in DEFAULT_PHOTO_OPTIONS if option["name"] == selected_photo_option)
            photo_width = photo_size_container.number_input("宽度", value=selected_option["photo_width"], disabled=True)
            photo_height = photo_size_container.number_input("高度", value=selected_option["photo_height"], disabled=True)
        margin = st.number_input("边距", min_value=10, value=10)
    with col2:
        paper_size_container = st.container(border=True)
        paper_size_container.write("相纸尺寸(单位：毫米)")
        selected_photo_option = paper_size_container.selectbox(
            "选择相纸尺寸", [option["name"] for option in DEFAULT_PAPER_OPTIONS]
        )
        if selected_photo_option == "自定义":
            paper_width = paper_size_container.number_input("宽度", min_value=1, value=127)
            paper_height = paper_size_container.number_input("高度", min_value=1, value=89)
        else:
            # Find the selected option
            selected_option = next(option for option in DEFAULT_PAPER_OPTIONS if option["name"] == selected_photo_option)
            paper_width = paper_size_container.number_input("宽度", value=selected_option["paper_width"], disabled=True)
            paper_height = paper_size_container.number_input("高度", value=selected_option["paper_height"], disabled=True)

    preview_button = st.button("预览", type="primary")
    if preview_button:
        with st.spinner("正在处理图片..."):
            photo_size = (photo_width, photo_height)
            paper_size = (paper_width, paper_height)
            collage = generate_photo_collage(photo_file, photo_size, paper_size, margin)
            st.image(image=collage, width=300)
            st.write("右键点击图片，选择“另存为”保存图片。")


if __name__ == "__main__":
    main()
