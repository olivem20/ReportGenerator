from PIL import ImageFont
import os

def get_font(size=40):
    # 1. Try bundled font (this is the key fix)
    local_font = "assets/fonts/Inter_18pt-Bold.ttf"

    if os.path.exists(local_font):
        return ImageFont.truetype(local_font, size)

    # 2. Fallback to system fonts (your old logic)
    import platform
    system = platform.system()

    if system == "Windows":
        font_candidates = [
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ]
    elif system == "Darwin":
        font_candidates = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
    else:
        font_candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]

    for font_path in font_candidates:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)

    return ImageFont.load_default()