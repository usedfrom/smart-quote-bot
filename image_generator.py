from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def create_quote_image(quote, suggestion):
    # Параметры изображения
    width, height = 1080, 1920
    background_path = "backgrounds/background.jpg"
    font_path = "fonts/NotoSerif-Regular.ttf"
    output_path = "temp_quote.png"
    
    # Загрузка фона
    background = Image.open(background_path).resize((width, height))
    
    # Создание объекта для рисования
    draw = ImageDraw.Draw(background)
    
    # Настройка шрифта
    font_size = 60
    font = ImageFont.truetype(font_path, font_size)
    
    # Подготовка текста
    quote_lines = textwrap.wrap(quote, width=30)
    suggestion_lines = textwrap.wrap(suggestion, width=30)
    
    # Расчет позиции текста
    y_text = height // 4
    max_width = width - 100  # Отступы по краям
    
    # Отрисовка цитаты (белый текст с тенью)
    for line in quote_lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        x = (width - text_width) // 2
        
        # Тень
        draw.text((x+2, y_text+2), line, font=font, fill="black")
        # Основной текст
        draw.text((x, y_text), line, font=font, fill="white")
        y_text += font_size + 10
    
    # Отрисовка предложения (меньший шрифт)
    font_size_suggestion = 40
    font_suggestion = ImageFont.truetype(font_path, font_size_suggestion)
    y_text += 50  # Отступ между цитатой и предложением
    
    for line in suggestion_lines:
        text_bbox = draw.textbbox((0, 0), line, font=font_suggestion)
        text_width = text_bbox[2] - text_bbox[0]
        x = (width - text_width) // 2
        
        # Тень
        draw.text((x+2, y_text+2), line, font=font_suggestion, fill="black")
        # Основной текст
        draw.text((x, y_text), line, font=font_suggestion, fill="white")
        y_text += font_size_suggestion + 10
    
    # Сохранение изображения
    background.save(output_path, "PNG")
    return output_path