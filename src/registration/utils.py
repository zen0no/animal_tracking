import pandas as pd


INIT_COLUMNS = ["name_folder", "class_predict", "date_registration", "bbox", "id", "count", "link"]


def init_result_df() -> pd.DataFrame:
    """Create a dataframe"""
    df = pd.DataFrame(columns=INIT_COLUMNS)

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

def connect_dfs(df, reg_df):
    """Add reqistration id to dataframes"""

    return df, reg_df
