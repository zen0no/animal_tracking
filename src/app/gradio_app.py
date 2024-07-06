from collections import Counter
import tempfile
import gradio as gr
import pandas as pd

from app.utils import extract_files, get_file_info, visualisation

from detection.predict import process_images
from detection.utils import get_spices, get_model_config

from registration.predict import process_dataframe, RESULT_COLUMN
from registration.utils import download_df, init_result_df, fill_result_df, connect_dfs, INIT_COLUMNS


DETECTION_DF = pd.DataFrame()
REGISTRATION_DF = pd.DataFrame()


def show_bboxes(id: int):
    row = DETECTION_DF.iloc[id]
   
    return visualisation(
        row['link'],
        row['bbox'],
        row['class_predict']
    )


def get_images(id: int):
    id = DETECTION_DF.iloc[id]['reg_id']
    row = REGISTRATION_DF.iloc[int(id)]

    images = [ (DETECTION_DF.iloc[det_id]['link'], f"id {det_id}")
        for det_id in row["ids"]
    ]

    return images


def visual_interface(id: int):
    return show_bboxes(id), get_images(id) 


def visible_component(inputs):
    return [gr.update(visible=True)]*4


def process_interface(file):
    global DETECTION_DF, REGISTRATION_DF

    images = extract_files(file)
    file_info = get_file_info(images)

    # create DataFrame
    df = init_result_df()
    df = fill_result_df(df, images=images)
    df = process_images(df)

    # return file info
    yield file_info, df, None, None, None

    reg_df = process_dataframe(df)

    # connect dataframes
    df, reg_df = connect_dfs(df, reg_df)

    # convert detection to CSV 
    detection_csv_path = download_df(df)
    regulation_csv_path = download_df(reg_df, drop_columns=["ids", "reg_id"])

    # Update global variables
    DETECTION_DF = df
    REGISTRATION_DF = reg_df

    yield file_info, df, reg_df , detection_csv_path, regulation_csv_path


def setting_interface():
    return get_spices(), get_model_config()


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Tab("Обработка"):
        with gr.Row():
            file_input = gr.File(label="Загрузите ZIP архив фотоловушек", type="filepath")
            file_info = gr.JSON(label="Информация загруженного архива")            

        detection_output = gr.Dataframe(label="Результаты детекции и классификации", wrap=True, headers=INIT_COLUMNS, visible=False)
        registration_output = gr.Dataframe(label="Результаты регистрации", wrap=True, headers=RESULT_COLUMN, visible=False)

        with gr.Row():
            det_download = gr.File(label="Скачать результаты детекции и классификации", visible=False)
            reg_download = gr.File(label="Скачать результаты регистрации", visible=False)


        file_input.upload(
            fn=visible_component,
            inputs=file_input, 
            outputs=[detection_output, registration_output, det_download, reg_download]
        ).then(
            process_interface, 
            inputs=file_input, 
            outputs=[file_info, detection_output, registration_output, det_download, reg_download]
        )

    with gr.Tab("Визуализация"):
        with gr.Row():
            with gr.Column():
                image_output = gr.AnnotatedImage()
                number = gr.Number(minimum=0, maximum=0, interactive=True)
                section_btn = gr.Button("Identify Sections")

                def update_maximum(value):
                    return gr.update(maximum=len(DETECTION_DF) - 1)

            with gr.Column():
                gallery = gr.Gallery(label="Также в регистрации", 
                           show_label=True)
            
            section_btn.click(
                    update_maximum,
                    inputs=None,
                    outputs=number
                ).then(visual_interface, number, [image_output, gallery])


    with gr.Tab("Настройки"):
        with gr.Row():
            spices = gr.JSON(label="Учитываемые особи")
            yolo_config = gr.JSON(label="Конфигурация модели")

        gr.Button("Получить конфигурации").click(setting_interface, outputs=[spices, yolo_config])
