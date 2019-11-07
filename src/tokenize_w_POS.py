
import pandas as pd

import nltk
from nltk import word_tokenize, pos_tag, pos_tag_sents

from nltk.collocations import *
nltk.download()

# open file. I used | as a seperator -- This version keeps the poorly labled columns
df = pd.read_csv('../data/data.csv', sep='|')

# preprocessing
df.drop(['Unnamed: 0','hostility'], axis=1, inplace=True)
df['description'] = df['description'].apply(lambda s: s.capitalize())
df.fillna("No information", inplace=True)
df.isnull().sum().sum()
df['description'] = df['description'].astype(str)

# Remove punctuation & tokenize
df['pos_tags']= ( df['description'].apply(word_tokenize).tolist() )
df['desc_wo_punct'] = df['description'].str.replace(r'[^\w\s]+', '')
df['POS'] = pos_tag_sents( df['desc_wo_punct'].apply(word_tokenize).tolist() )

# And now save it as a new file
