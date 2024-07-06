import pandas as pd


def convert_to_seconds(dataframe):
    dataframe['date_registration'] = pd.to_datetime(dataframe['date_registration'])
    dataframe['sec_registration'] = (((dataframe['date_registration'].dt.month * 12 +
                                     dataframe['date_registration'].dt.day) * 24 +
                                     dataframe['date_registration'].dt.hour) * 60 \
                                    + dataframe['date_registration'].dt.minute) * 60 \
                                    + dataframe['date_registration'].dt.second


def init_result_df() -> pd.DataFrame:
    """Create a dataframe"""
    columns = ["name_folder", "class_predict", "date_registration", "bbox", "id", "count", "link"]
    df = pd.DataFrame(columns=columns)

    return df


def fill_result_df(df: pd.DataFrame, images: list[str]) -> pd.DataFrame:
    """Fill the dataframe"""
    for i, image_path in enumerate(images):
        name_folder = image_path.split("/")[-2]  # Извлекаем название папки
        link = image_path
        id = i # Порядковый номер
        
        # Заполняем другие поля пустыми значениями или нулями
        class_predict = ""
        date_registration = pd.NaT
        bbox = ""
        count = 0
        
        df.loc[len(df)] = [name_folder, class_predict, date_registration, bbox, id, count, link]

    return df