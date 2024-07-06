import tempfile
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
    """Add registration id to dataframes"""
    # Add reg_id to reg_df
    reg_df['reg_id'] = reg_df.index

    # Create a mapping from detection id to reg_id
    det_to_reg_map = {}
    for idx, row in reg_df.iterrows():
        for det_id in row['ids']:
            det_to_reg_map[det_id] = row['reg_id']
    
    # Add reg_id to df
    df['reg_id'] = df['id'].map(det_to_reg_map)
    
    return df, reg_df

def download_df(df, drop_columns=None):
    if drop_columns is not None:
        df = df.drop(columns=["ids", "reg_id"], axis=1)

    csv_path = tempfile.mktemp(suffix=".csv")
    df.to_csv(csv_path, index=False)

    return csv_path
