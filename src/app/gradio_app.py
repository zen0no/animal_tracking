import tempfile
import gradio as gr
import pandas as pd

from app.utils import extract_files, get_file_info, visualisation

from detection.predict import process_images
from detection.utils import get_spices, get_model_config

from registration.predict import process_dataframe, RESULT_COLUMN
from registration.utils import init_result_df, fill_result_df, INIT_COLUMNS


DETECTION_DF = pd.DataFrame()

def show_bboxes(id: int):
    row = DETECTION_DF.iloc[id]
   
    return visualisation(
        row['link'],
        row['bbox'],
        row['class_predict']
    )

def visible_component(inputs):
    return [gr.update(visible=True)]*4

def process_interface(file):
    global DETECTION_DF

    images = extract_files(file)
    file_info = get_file_info(images)

    # create DataFrame
    df = init_result_df()
    df = fill_result_df(df, images=images)
    df = process_images(df)

    # return file info
    yield file_info, df, None, None, None

    # reg_df = process_dataframe(df)

    # convert detection to CSV 
    detection_csv_path = tempfile.mktemp(suffix=".csv")
    df.to_csv(detection_csv_path, index=False)

    # convert regualtion to SCV
    regulation_csv_path = tempfile.mktemp(suffix=".csv")
    df.to_csv(regulation_csv_path, index=False)

    # Update global variables
    DETECTION_DF = df

    yield file_info, df, None , detection_csv_path, None


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
            outputs=[file_info, detection_output, registration_output, det_download, reg_download])

    with gr.Tab("Визуализация"):
        image_output = gr.AnnotatedImage()
        number = gr.Number(minimum=0, maximum=0, interactive=True)
        section_btn = gr.Button("Identify Sections")
        section_btn.click(
            lambda value: gr.update(maximum=len(DETECTION_DF)-1),
            inputs= number,
            outputs=number
        ).then(show_bboxes, number, image_output)


    with gr.Tab("Настройки"):
        with gr.Row():
            spices = gr.JSON(label="Учитываемые особи")
            yolo_config = gr.JSON(label="Конфигурация модели")

        gr.Button("Получить конфигурации").click(setting_interface, outputs=[spices, yolo_config])
