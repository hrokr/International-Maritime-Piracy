from nltk.stem.wordnet import WordNetLemmatizer

import spacy
from spacy.lang.en import English
import nltk

nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import random
from gensim import corpora
import gensim
import pyLDAvis.gensim

print("Updating stopwords")

with open('../data/add_num_stops.txt', 'r') as f:
    s = [i for i in f]
    add_numerical_stops = set(s)

 
nlp = spacy.load("en")
nlp.Defaults.stop_words |= add_numerical_stops

c = nlp.Defaults.stop_words

# print("Tokenizing words")

# parser = English()

# print('Loading functions')
# def tokenize(text):
#     lda_tokens = []
#     tokens = parser(text)
#     for token in tokens:
#         if token.orth_.isspace():
#             continue
#         elif token.like_url:
#             lda_tokens.append('URL')
#         else:
#             lda_tokens.append(token.lower_)
#     return lda_tokens


# def get_lemma(word):
#     lemma = wn.morphy(word)
#     if lemma is None:
#         return word
#     else:
#         return lemma
    

# def get_lemma2(word):
#     return WordNetLemmatizer().lemmatize(word)


# def prepare_text_for_lda(text):
#     tokens = tokenize(text)
#     tokens = [token for token in tokens if len(token) > 4]
#     tokens = [token for token in tokens]
#     tokens = [get_lemma(token) for token in tokens]
#     return tokens


# print("opening file") 
# text_data = []
# with open('../data/tokenized.csv') as f:
#     for line in f:
#         tokens = prepare_text_for_lda(line)
#         if random.random() > .99:
#             print(tokens)
#             text_data.append(tokens)

# print("5")


# dictionary = corpora.Dictionary(text_data)
# corpus = [dictionary.doc2bow(text) for text in text_data]
# import pickle
# pickle.dump(corpus, open('corpus.pkl', 'wb'))
# dictionary.save('dictionary.gensim')

# print("6")

# NUM_TOPICS = 4
# ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=50)
# ldamodel.save('model4_50-.gensim')
# topics = ldamodel.print_topics(num_words=10)
# for topic in topics:
#     print(topic)
# print("---------------------------------------\n")
# print("7")

# new_doc = 'Algerian pirates board M/V Taiuga Khan off Tunesaian waters. TWIF responds. 4 pirates, 2 crew KIA'
# new_doc = prepare_text_for_lda(new_doc)
# new_doc_bow = dictionary.doc2bow(new_doc)
# print(new_doc_bow)
# print(ldamodel.get_document_topics(new_doc_bow))

# print("Running model with 3 topics @ 50 passes")

# ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 3, id2word=dictionary, passes=50)
# ldamodel.save('model3_50.gensim')
# topics = ldamodel.print_topics(num_words=10)
# for topic in topics:
#     print(topic)

# print("Running model with 5 topics @ 50 passes")

# ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 5, id2word=dictionary, passes=50)
# ldamodel.save('model5_50.gensim')
# topics = ldamodel.print_topics(num_words=4)
# for topic in topics:
#     print(topic)

# print("10")

# # dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
# # corpus = pickle.load(open('corpus.pkl', 'rb'))
# # lda = gensim.models.ldamodel.LdaModel.load('model5.gensim')

# # print("11")

# # lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)
# # pyLDAvis.display(lda_display)
# # print("12")

# # lda3 = gensim.models.ldamodel.LdaModel.load('model3.gensim')
# # lda_display3 = pyLDAvis.gensim.prepare(lda3, corpus, dictionary, sort_topics=False)
# # pyLDAvis.display(lda_display3)

# # print("done")