import gradio as gr
from utils import get_spices, get_model_config


def process_interface(file):
    pass


def setting_interface():
    return get_spices(), get_model_config()


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Tab("Обработка"):
        with gr.Row():
            file_input = gr.File(label="Загрузите ZIP архив с фотками", type="filepath")
            image_output = gr.Gallery(label="Примеры фотографий")
        dataframe_output = gr.Dataframe(label="Результаты обработки")

        file_input.upload(process_interface, inputs=file_input, outputs=[image_output, dataframe_output])

    with gr.Tab("Настройки"):
        with gr.Row():
            spices = gr.JSON(label="Учитываемые особи")
            yolo_config = gr.JSON(label="Конфигурация модели")

        
        gr.Button("Получить конфигурации YOLO").click(setting_interface, outputs=[spices, yolo_config])
        