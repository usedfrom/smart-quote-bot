from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

def create_image(quote: str, suggestion: str) -> str:
    image = Image.open("backgrounds/background.jpg")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("fonts/NotoSerif-Regular.ttf", size=40)
    
    max_width = 900
    quote_lines = textwrap.wrap(quote, width=30)
    suggestion_lines = textwrap.wrap(suggestion, width=30)
    
    y_text = 200
    for line in quote_lines:
        draw.text((100, y_text), line, font=font, fill=(255, 255, 255))
        y_text += 60
    y_text += 40
    for line in suggestion_lines:
        draw.text((100, y_text), line, font=font, fill=(200, 200, 200))
        y_text += 60
    
    output_path = "output_quote.png"
    image.save(output_path)
    return output_path
