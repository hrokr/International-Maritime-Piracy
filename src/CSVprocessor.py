import pandas as pd


class Processor(csv_file):
    """
    Reads in the downloaded .csv NGA Anti Shipping Messages and parses the content
    """

    def __init__(self, name):
        self.name = name

    def getData(self, path):
        df = pd.read_csv('../data/piracy.csv')

    def drop_NaN_Cols(self, data):
        for col in frame:
            if data['Unnamed: 8'].unique() == 'array([nan])' #<--8 also needs to be generalized
                data.drop(['Unnamed: 8'], axis=1, inplace=True)

    def splitLatLong (self, data):
        data = data.join(data['position'].str.split(expand=True)).rename(columns={0:'Latitude', 1:'Longitude'})
        data.drop('position', axis=1, inplace=True)

    def dms2dd(self, data):
        degrees, minutes, seconds, direction = re.split('[°\'"]+', s)
        dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
        if direction in ('S', 'W'):
            dd *= -1
        return dd

        data['Latitude'] = data['Latitude'].apply(dms2dd)
        data['Longitude'] = data['Longitude'].apply(dms2dd)     

    def saveData(self):
        df.to_csv(('../data/data_pipe.csv'), sep='|', index=False)
