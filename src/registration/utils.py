def convert_to_seconds(dataframe):
  dataframe['date_registration'] = pd.to_datetime(dataframe['date_registration'])
  dataframe['sec_registration'] = (((dataframe['date_registration'].dt.month * 12 +
                                     dataframe['date_registration'].dt.day) * 24 +
                                     dataframe['date_registration'].dt.hour) * 60 \
                                    + dataframe['date_registration'].dt.minute) * 60 \
                                    + dataframe['date_registration'].dt.second