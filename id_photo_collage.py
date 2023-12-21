import argparse
from PIL import Image


def pixels_to_cm(pixels, dpi):
    inches = pixels / dpi
    cm = inches * 2.54
    return cm


def pixels_to_mm(pixels, dpi):
    inches = pixels / dpi
    mm = inches * 25.4
    return mm


def cm_to_pixels(cm, dpi):
    inches = cm / 2.54
    pixels = inches * dpi
    return int(pixels)


def mm_to_pixels(mm, dpi):
    inches = mm / 25.4
    pixels = inches * dpi
    return int(pixels)


def generate_photo_collage(photo_path, photo_size, paper_size, margin):
    # 打开照片
    photo = Image.open(photo_path)

    # 调整照片尺寸
    photo = photo.resize(
        (mm_to_pixels(photo_size[0], 300), mm_to_pixels(photo_size[1], 300)),
        Image.Resampling.LANCZOS,
    )

    # 计算每张证件照的尺寸
    photo_width, photo_height = photo.size

    # 计算相纸尺寸
    paper_width_mm, paper_height_mm = paper_size

    # 计算相纸的像素尺寸
    paper_width = mm_to_pixels(paper_width_mm, 300)
    paper_height = mm_to_pixels(paper_height_mm, 300)

    # 计算相纸横向纵向各可以容纳几张证件照
    rows = int((paper_height - margin) // (photo_height + margin))
    cols = int((paper_width - margin) // (photo_width + margin))

    print(rows, cols)

    collage = Image.new("RGB", (paper_width, paper_height), (255, 255, 255))

    # 将证件照按照排列顺序粘贴到相纸上
    for row in range(rows):
        for col in range(cols):
            x = int(margin + col * (photo_width + margin))
            y = int(margin + row * (photo_height + margin))
            print(photo)
            collage.paste(photo, (x, y))

    # 保存生成的相纸
    collage.save("photo_collage.jpg")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate photo collage.")
    parser.add_argument("photo_path", type=str, help="Path to the input photo.")
    parser.add_argument(
        "photo_width", type=float, help="Width of the photo in millimeters."
    )
    parser.add_argument(
        "photo_height", type=float, help="Height of the photo in millimeters."
    )
    parser.add_argument(
        "paper_width", type=float, help="Width of the paper in millimeters."
    )
    parser.add_argument(
        "paper_height", type=float, help="Height of the paper in millimeters."
    )
    parser.add_argument(
        "margin", type=float, help="Margin between photos in millimeters."
    )
    args = parser.parse_args()

    # 调用函数生成证件照排列
    photo_size = (args.photo_width, args.photo_height)
    paper_size = (args.paper_width, args.paper_height)
    generate_photo_collage(args.photo_path, photo_size, paper_size, args.margin)
