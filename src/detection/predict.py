import gc
import pandas as pd
from PIL import Image

from detection.utils import predict, get_date_from_exif, MODEL
from env.env import BATCH_SIZE


def load_image(image_path):
    """Load image from a given path."""
    return Image.open(image_path)


def process_images(df: pd.DataFrame):
    """Process images in batches and update DataFrame with predictions."""
    image_paths = df['link'].tolist()
    num_images = len(image_paths)
    batch_size = BATCH_SIZE  # Используем BATCH_SIZE из вашего конфигурационного файла

    all_classes = []
    all_bboxes = []
    all_ids = []
    all_date = []

    for i in range(0, num_images, batch_size):
        batch_paths = image_paths[i:i + batch_size]
        
        # Загрузка изображений
        images = [load_image(p) for p in batch_paths]
        
        # Выполнение предсказаний
        predictions = predict(MODEL, images)
        
        all_classes.extend(predictions['class_predict'])
        all_bboxes.extend(predictions['bbox'])
        all_ids.extend(predictions['id'])
        all_date.extend([get_date_from_exif(image) for image in images])

        del images
        gc.collect()

    # Обновление DataFrame
    df['class_predict'] = pd.Series(all_classes)
    df['bbox'] = pd.Series(all_bboxes)
    df['count'] = pd.Series([len(ids) for ids in all_ids])
    df['date_registration'] = pd.Series(all_date)
    
    return df