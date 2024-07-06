import gradio as gr
import pandas as pd
import time

from app.utils import get_model_config, extract_files, get_file_info
from detection.utils import get_spices
from registration.utils import init_result_df, fill_result_df


def process_interface(file):
    images = extract_files(file)
    file_info = get_file_info(images)

    # create DataFrame
    df = init_result_df()
    df = fill_result_df(df, images=images)

    # return file info
    yield file_info, [], df


    time.sleep(2)
    yield file_info, [], df


def setting_interface():
    return get_spices(), get_model_config()


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Tab("Обработка"):
        with gr.Row():
            file_input = gr.File(label="Загрузите ZIP архив фотоловушек", type="filepath")
            file_info = gr.JSON(label="Информация загруженного архива")
        image_output = gr.Gallery(label="Примеры фотографий")
        dataframe_output = gr.Dataframe(label="Результаты обработки", type="pandas", wrap=True)

        file_input.upload(process_interface, inputs=file_input, outputs=[file_info, image_output, dataframe_output])

    with gr.Tab("Настройки"):
        with gr.Row():
            spices = gr.JSON(label="Учитываемые особи")
            yolo_config = gr.JSON(label="Конфигурация модели")

        gr.Button("Получить конфигурации").click(setting_interface, outputs=[spices, yolo_config])
