import pandas as pd


TRESHOLD = 30 * 60
RESULT_COLUMN = ['folder_name', 'class', 'start', 'end', 'max_count', 'id']


def convert_to_seconds(dataframe):
    dataframe['date_registration'] = pd.to_datetime(dataframe['date_registration'])
    dataframe['sec_registration'] = (((dataframe['date_registration'].dt.month * 12 +
                                        dataframe['date_registration'].dt.day) * 24 +
                                        dataframe['date_registration'].dt.hour) * 60 \
                                        + dataframe['date_registration'].dt.minute) * 60 \
                                        + dataframe['date_registration'].dt.second

def get_registration(data, ind):
    end, max_count, ids = ind, 0, []
    for i in data.index[ind : data.shape[0]]:
        if data.loc[i, 'sec_registration'] - data.loc[ind, 'sec_registration'] > TRESHOLD:
            break
        elif data.loc[i, 'class_predict'] == data.loc[ind, 'class_predict']:
            end = i
            max_count = max(max_count, data.loc[i, 'count'])
            data.loc[i, 'count'] = 0
            ids.append(data.loc[i, 'id'])

    return {'class': data.loc[ind, 'class_predict'],
            'start': data.loc[ind, 'date_registration'],
            'end': data.loc[end, 'date_registration'],
            'max_count': max_count,
            'id': ids}

def handle(cam):
    folder_regs = pd.DataFrame(columns=['class', 'start', 'end', 'max_count', 'id'])
    while cam['count'].sum() > 0:
        ind = cam.index[cam['count'] > 0].tolist()[0]
        new_reg = get_registration(cam, ind)

        if new_reg is not None:
            folder_regs = pd.concat([folder_regs, pd.Series(new_reg).to_frame().T], ignore_index=True)
    return folder_regs


def process_dataframe(df: pd.DataFrame):
    df = df.convert_dtypes()
    overall_regs = pd.DataFrame(columns=RESULT_COLUMN)

    for name_folder in df['name_folder'].unique():
        cam_data = df[df['name_folder'] == name_folder][['class_predict', 'date_registration', 'count', 'id']]
        convert_to_seconds(cam_data)
        cam_data = cam_data.sort_values(by='sec_registration').dropna(axis=0).reset_index()

        folder_regs = handle(cam_data)
        folder_regs = folder_regs.assign(folder_name=pd.Series([None] * folder_regs.shape[0]).values)
        folder_regs['folder_name'] = name_folder
        overall_regs = pd.concat([overall_regs, folder_regs], ignore_index=True)

    return overall_regs
