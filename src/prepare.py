import pandas as pd

# open file. I used | as a seperator -- This version keeps the poorly labled columns
df = pd.read_csv('../data/data_pipe.csv', sep='|')

# preprocessing
df.drop(['Unnamed: 0', 'hostility'], axis=1, inplace=True)
df['description'] = df['description'].apply(lambda s: s.capitalize())
df.fillna("No information", inplace=True)
df.isnull().sum().sum()
df['description'] = df['description'].astype(str)


# And now save it as a new file
df.to_csv('../data/step2.csv', sep='|', encoding='utf-8')
print("file cleaned")