import os
from st_pages import Page, show_pages, add_page_title

MODELS_PATH = os.path.join(os.path.dirname(__file__), "models")
if not os.path.exists(MODELS_PATH):
    os.makedirs(MODELS_PATH)
os.environ["U2NET_HOME"] = MODELS_PATH


# Optional -- adds the title and icon to the current page
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("web_pages/collage_page.py", "证件照拼贴", "🏠"),
        Page("web_pages/remove_background_page.py", "去除图片背景", ":books:"),
    ]
)
