import gradio as gr
import zipfile
import pandas as pd
import os
import json
from PIL import Image

def process_zip(file):
    if file is None:
        return None, None

    # Создаем временную папку для извлечения файлов
    with zipfile.ZipFile(file.name, 'r') as zip_ref:
        zip_ref.extractall('temp_images')

    # Считываем извлеченные файлы и обрабатываем их
    images = []
    data = []
    for filename in os.listdir('temp_images'):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join('temp_images', filename)
            img = Image.open(img_path)
            images.append(img)
            # Пример данных об обработке изображений
            data.append({
                "filename": filename,
                "width": img.width,
                "height": img.height,
                "format": img.format
            })
    
    # Создаем датафрейм с результатами обработки
    df = pd.DataFrame(data)
    
    return images, df

def get_yolo_config():
    # Пример конфигурации для YOLO модели
    yolo_config = {
        "model": "yolov5",
        "confidence_threshold": 0.5,
        "nms_threshold": 0.4,
        "input_size": (640, 640)
    }
    return json.dumps(yolo_config, indent=4)

with gr.Blocks(theme=gr.themes.Glass()) as demo:
    with gr.Tab("Обработка"):
        file_input = gr.File(label="Загрузите ZIP архив с фотками", type="file")
        image_output = gr.Gallery(label="Примеры фотографий")
        dataframe_output = gr.Dataframe(label="Результаты обработки")

        file_input.upload(process_zip, inputs=file_input, outputs=[image_output, dataframe_output])

    with gr.Tab("Настройки"):
        yolo_config_output = gr.JSON(label="Конфигурации YOLO")
        
        gr.Button("Получить конфигурации YOLO").click(get_yolo_config, outputs=yolo_config_output)
