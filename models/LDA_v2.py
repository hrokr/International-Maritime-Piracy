import warnings
import pandas as pd
import numpy as np
np.random.seed(2018)

import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt

from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split

import gensim
from gensim import corpora, models
from gensim.parsing.preprocessing import STOPWORDS
from gensim.parsing.preprocessing import remove_stopwords 
from gensim.utils import simple_preprocess

import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
from sklearn.feature_extraction.text import CountVectorizer
# NumPy - multidimensional arrays, matrices, and high-level mathematical formulas

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

warnings.filterwarnings("ignore",category=DeprecationWarning)

df = pd.read_csv('../data/data_pipe.csv', sep='|', encoding = "utf-8");
df_text = df['description']
df_text['index'] = df_text.index
docs = df_text


def lemmatize_stemming(text):
    stemmer = PorterStemmer()
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

# parse docs into individual words ignoring words that are less than 3 letters long
# and stopwords: him, her, them, for, there, ect since "their" is not a topic.
# then append the tolkens into a list

with open('../data/more_stop_words.txt', 'r') as f:
    customize_stop_words = f.read().replace('\n', '')

with open('../data/add_num_stops.txt', 'r') as f:
    customize_stop_nums = f.read().replace('\n', '')

combined_stops = [customize_stop_words + customize_stop_nums]

from gensim.parsing.preprocessing import STOPWORDS
expanded_stop_words = STOPWORDS.union(set(combined_stops))
# print(expanded_stop_words, type(expanded_stop_words))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in expanded_stop_words and len(token) > 3:
            nltk.bigrams(token)
            result.append(lemmatize_stemming(token))
    return result

# look at a random row 4310 and see if things worked out
# note that the document created was already preprocessed

print (df.loc[4310,'description'])

words = []
for word in doc_sample.split(' '):
    words.append(word)
print(words)
print('\n\n tokenized and lemmatized document: ')
print(preprocess(doc_sample))

# let’s look at ten rows passed through the lemmatize stemming and preprocess

documents = documents.dropna()
processed_docs = documents['documents'].map(preprocess)
processed_docs[:10]


# we create a dictionary of all the words in the csv by iterating through
# contains the number of times a word appears in the training set.

dictionary_valid = gensim.corpora.Dictionary(processed_docs[20000:])
count = 0
for k, v in dictionary_valid.iteritems():
    print(k, v)
    count += 1
    if count > 30:
        break
        
# we create a dictionary of all the words in the csv by iterating through
# contains the number of times a word appears in the training set.

dictionary_test = gensim.corpora.Dictionary(processed_docs[:20000])
count = 0
for k, v in dictionary_test.iteritems():
    print(k, v)
    count += 1
    if count > 30:
        break
        
# we want to throw out words that are so frequent that they tell us little about the topic 
# as well as words that are too infrequent >15 rows then keep just 100,000 words

dictionary_valid.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

# we want to throw out words that are so frequent that they tell us little about the topic 
# as well as words that are too infrequent >15 rows then keep just 100,000 words

dictionary_test.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

# the words become numbers and are then counted for frequency
# consider a random row 4310 - it has 8 words word indexed 2 shows up once
# preview the bag of words

bow_corpus_valid = [dictionary_valid.doc2bow(doc) for doc in processed_docs]
bow_corpus_valid[4310]

# the words become numbers and are then counted for frequency
# consider a random row 4310 - it has 8 words word indexed 2 shows up once
# preview the bag of words

bow_corpus_test = [dictionary_test.doc2bow(doc) for doc in processed_docs]
bow_corpus_test[4310]

# same thing in more words

bow_doc_4310 = bow_corpus_test[4310]
for i in range(len(bow_doc_4310)):
    print("Word {} (\"{}\") appears {} time.".format(bow_doc_4310[i][0], 
                                               dictionary_test[bow_doc_4310[i][0]], 
bow_doc_4310[i][1]))

mallet_path = 'C:/mallet/mallet-2.0.8/bin/mallet.bat'

ldamallet_test = gensim.models.wrappers.LdaMallet(mallet_path, corpus=bow_corpus_test, num_topics=20, id2word=dictionary_test)

result = (ldamallet_test.show_topics(num_topics=20, num_words=10,formatted=False))
for each in result:
    print (each)
    
mallet_path = 'C:/mallet/mallet-2.0.8/bin/mallet.bat'

ldamallet_valid = gensim.models.wrappers.LdaMallet(mallet_path, corpus=bow_corpus_valid, num_topics=20, id2word=dictionary_valid)

result = (ldamallet_valid.show_topics(num_topics=20, num_words=10,formatted=False))
for each in result:
    print (each)
    
# Show Topics
for idx, topic in ldamallet_test.print_topics(-1):
   print('Topic: {} \nWords: {}'.format(idx, topic))
   
# Show Topics
for idx, topic in ldamallet_valid.print_topics(-1):
   print('Topic: {} \nWords: {}'.format(idx, topic))
   
# check out the topics - 30 words - 20 topics

ldamallet_valid.print_topics(idx, 30)

# check out the topics - 30 words - 20 topics

ldamallet_test.print_topics(idx, 30)

# Compute Coherence Score
coherence_model_ldamallet_valid = CoherenceModel(model=ldamallet_valid, texts=processed_docs, dictionary=dictionary_valid, coherence='c_v')
coherence_ldamallet_valid = coherence_model_ldamallet_valid.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet_valid)

# Compute Coherence Score
coherence_model_ldamallet_test = CoherenceModel(model=ldamallet_test, texts=processed_docs, dictionary=dictionary_test, coherence='c_v')
coherence_ldamallet_test = coherence_model_ldamallet_test.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet_test)