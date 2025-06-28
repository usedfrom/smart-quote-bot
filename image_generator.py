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
    
    # Настройка шрифтов
    quote_font_size = 80  # Увеличенный размер шрифта для цитаты
    suggestion_font_size = 50  # Увеличенный размер шрифта для предложения
    quote_font = ImageFont.truetype(font_path, quote_font_size)
    suggestion_font = ImageFont.truetype(font_path, suggestion_font_size)
    
    # Параметры разбиения текста
    max_width = width - 100  # Отступы по краям (50 пикселей с каждой стороны)
    quote_wrap_width = 25  # Количество символов для переноса цитаты
    suggestion_wrap_width = 35  # Количество символов для переноса предложения
    
    # Разбиение текста на строки
    quote_lines = textwrap.wrap(quote, width=quote_wrap_width)
    suggestion_lines = textwrap.wrap(suggestion, width=suggestion_wrap_width)
    
    # Расчёт высоты текста для центрирования
    quote_height = len(quote_lines) * (quote_font_size + 10)  # Высота блока цитаты
    suggestion_height = len(suggestion_lines) * (suggestion_font_size + 10)  # Высота блока предложения
    total_text_height = quote_height + suggestion_height + 50  # Отступ между блоками
    
    # Начальная позиция Y для центрирования всего текста
    y_text = (height - total_text_height) // 2
    
    # Отрисовка цитаты (белый текст с тенью)
    for line in quote_lines:
        text_bbox = draw.textbbox((0, 0), line, font=quote_font)
        text_width = text_bbox[2] - text_bbox[0]
        x = (width - text_width) // 2
        
        # Тень
        draw.text((x + 3, y_text + 3), line, font=quote_font, fill="black")
        # Основной текст
        draw.text((x, y_text), line, font=quote_font, fill="white")
        y_text += quote_font_size + 10
    
    # Отступ между цитатой и предложением
    y_text += 50
    
    # Отрисовка предложения (белый текст с тенью)
    for line in suggestion_lines:
        text_bbox = draw.textbbox((0, 0), line, font=suggestion_font)
        text_width = text_bbox[2] - text_bbox[0]
        x = (width - text_width) // 2
        
        # Тень
        draw.text((x + 3, y_text + 3), line, font=suggestion_font, fill="black")
        # Основной текст
        draw.text((x, y_text), line, font=suggestion_font, fill="white")
        y_text += suggestion_font_size + 10
    
    # Сохранение изображения
    background.save(output_path, "PNG")
    return output_path
    
    # Сохранение изображения
    background.save(output_path, "PNG")
    return output_path
