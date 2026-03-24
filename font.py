from PIL import ImageFont
import os

def get_font(size=40):
    local_font = "assets/fonts/Inter_18pt-Bold.ttf"

    if not os.path.exists(local_font):
        raise FileNotFoundError(f"Font file not found: {local_font}")

    return ImageFont.truetype(local_font, size)