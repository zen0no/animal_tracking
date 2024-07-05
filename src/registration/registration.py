import pandas as pd


from src.registration.utils import convert_to_seconds


TRESHOLD = 30 * 60


def get_registration(data, ind):
  end, max_count = ind, 0
  for i in data.index[ind : data.shape[0]]:
    if data.loc[i, 'sec_registration'] - data.loc[ind, 'sec_registration'] > TRESHOLD:
      break
    elif data.loc[i, 'class_predict'] == data.loc[ind, 'class_predict']:
      end = i
      max_count = max(max_count, data.loc[i, 'count'])
      data.loc[i, 'count'] = 0

  return {'class': data.loc[ind, 'class_predict'],
          'start': data.loc[ind, 'date_registration'],
          'end': data.loc[end, 'date_registration'], 'max_count': max_count}


def handle(cam):
  folder_regs = pd.DataFrame(columns=['class', 'start', 'end', 'max_count'])
  while cam['count'].sum() > 0:
    ind = cam.index[cam['count'] > 0].tolist()[0]
    new_reg = get_registration(cam, ind)

    if new_reg is not None:
      folder_regs = pd.concat([folder_regs, pd.Series(new_reg).to_frame().T], ignore_index=True)
  return folder_regs


def get_overall_registrations(dataframe):
  overall_regs = pd.DataFrame(columns=['folder_name', 'class', 'start', 'end', 'max_count'])

  for name_folder in dataframe['name_folder'].unique():
    cam_data = dataframe[dataframe['name_folder'] == name_folder][['class_predict', 'date_registration', 'count']]
    convert_to_seconds(cam_data)
    cam_data = cam_data.sort_values(by='sec_registration').dropna(axis=0).reset_index()
    # print(cam_data.head(20))
    print(name_folder)
    folder_regs = handle(cam_data)
    folder_regs = folder_regs.assign(folder_name=pd.Series([None] * folder_regs.shape[0]).values)
    folder_regs['folder_name'] = name_folder
    overall_regs = pd.concat([overall_regs, folder_regs], ignore_index=True)
    # print(overall_regs)
    # break
  overall_regs.to_csv('overall.csv')
  return overall_regs
