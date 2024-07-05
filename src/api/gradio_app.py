import gradio as gr
import pandas as pd

from utils import get_spices, get_model_config, extract_files


def process_interface(file):
    files = extract_files(file)

    return [], pd.DataFrame([])


def setting_interface():
    return get_spices(), get_model_config()


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Tab("Обработка"):
        with gr.Row():
            file_input = gr.File(label="Загрузите ZIP архив фотоловушек", type="filepath")
            file_info = gr.JSON(label="Информация загруженного архива.", value="""{"фотоловушки": {"1":150, "2": 200}}""")
        image_output = gr.Gallery(label="Примеры фотографий")
        dataframe_output = gr.Dataframe(label="Результаты обработки",type="pandas")

        file_input.upload(process_interface, inputs=file_input, outputs=[image_output, dataframe_output])

    with gr.Tab("Настройки"):
        with gr.Row():
            spices = gr.JSON(label="Учитываемые особи")
            yolo_config = gr.JSON(label="Конфигурация модели")

        gr.Button("Получить конфигурации YOLO").click(setting_interface, outputs=[spices, yolo_config])
