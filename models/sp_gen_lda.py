import os
import codecs
import json
import itertools as it
import random
import warnings
import pickle

import pandas as pd

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn

import spacy
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS


import pyLDAvis
import pyLDAvis.gensim
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence
from gensim import corpora
from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamulticore import LdaMulticore

data_directory = os.path.join('../data', 'mungedASAM.json')  

events = [i for i in range(7843)]
event_ids = set(events)

event_descriptions=set()
with codecs.open(data_directory, encoding='utf_8') as f:
     for event_json in f:
        event = json.loads(event_json)
        for item in event:         
           event_descriptions.add(item[u'description'])


intermediate_directory = os.path.join('../data')

event_txt_filepath = os.path.join(intermediate_directory,
                                   'all_descriptions.txt')

print("Updating stopwords")

nlp = spacy.load("en")

spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

with open('../data/add_num_stops.txt', 'r') as f:
    customize_stop_words = s = [i for i in f]
    add_numerical_stops = set(s)
    spacy_stopwords |= add_numerical_stops

with open('../data/more_stop_words.txt', 'r') as f:
    customize_stop_words = s = [i for i in f]
    more_stop_words = set(s) 
    spacy_stopwords |= more_stop_words


# if verbose=True:
#     print('Number of stop words: %d' % len(spacy_stopwords))
#     print('First ten stop words: %s' % list(spacy_stopwords)[:1000])



#     spacy_nlp.vocab[w].is_stop = Truedoc = spacy_nlp(article)
# tokens = [token.text for token in doc if not token.is_stop]

# for stopword in my_stop_words:
#     lexeme = nlp.vocab[stopword]
#     lexeme.is_stop = True




count = 0

with codecs.open(event_txt_filepath, 'w', encoding='utf_8') as event_txt_file:
    with codecs.open(data_directory, encoding='utf_8') as event_json_file:
        for event_json in event_json_file:                
            event = json.loads(event_json)
            for item in event:
                event_txt_file.write(item[u'description'].replace('\n', '\\n') + '\n')
                count += 1 

with codecs.open(event_txt_filepath, encoding='utf_8') as event_txt_file:
    for event_count, line in enumerate(event_txt_file):
        pass


with codecs.open(event_txt_filepath, encoding='utf_8') as f:
    sample_review = list(it.islice(f, 8, 9))[0]
    sample_review = sample_review.replace('\\n', '\n')
        
#print (f"Showing sample {sample_review}")

#%%time
parsed_review = nlp(sample_review)

#print("Parsing sentences")
# for num, sentence in enumerate(parsed_review.sents):
#     print ('Sentence {}:'.format(num + 1))
#     print (sentence)
#     print ('')

# print("showing parsed entites")
# for num, entity in enumerate(parsed_review.ents):
#     print ('Entity {}:'.format(num + 1), entity, '-', entity.label_)
#     print ('')

# Tokenization
token_text = [token.orth_ for token in parsed_review]
token_pos = [token.pos_ for token in parsed_review]

pd.DataFrame(zip(token_text, token_pos),
             columns=['token_text', 'part_of_speech'])


# Lemmatization
token_lemma = [token.lemma_ for token in parsed_review]
token_shape = [token.shape_ for token in parsed_review]

pd.DataFrame(zip(token_text, token_lemma, token_shape),
             columns=['token_text', 'token_lemma', 'token_shape'])

# Types (token and entity typs; inside outside marking)

token_attributes = [(token.orth_,
                     token.prob,
                     token.is_stop,
                     token.is_punct,
                     token.is_space,
                     token.like_num,
                     token.is_oov)
                    for token in parsed_review]

df = pd.DataFrame(token_attributes,
                  columns=['text',
                           'log_probability',
                           'stop?',
                           'punctuation?',
                           'whitespace?',
                           'number?',
                           'out of vocab.?'])

df.loc[:, 'stop?':'out of vocab.?'] = (df.loc[:, 'stop?':'out of vocab.?']
                                       .applymap(lambda x: u'Yes' if x else u''))


# helper functions
def punct_space(token):
    """
    helper function to eliminate tokens
    that are pure punctuation or whitespace
    """
    
    return token.is_punct or token.is_space

def line_review(filename):
    """
    generator function to read in reviews from the file
    and un-escape the original line breaks in the text
    """
    
    with codecs.open(filename, encoding='utf_8') as f:
        for review in f:
            yield review.replace('\\n', '\n')
            
def lemmatized_sentence_corpus(filename):
    """
    generator function to use spaCy to parse reviews,
    lemmatize the text, and yield sentences
    """
    
    for parsed_review in nlp.pipe(line_review(filename),
                                  batch_size=10000, n_threads=4): # I have an old macbook. But I love it.
        
        for sent in parsed_review.sents:
            yield u' '.join([token.lemma_ for token in sent
                             if not punct_space(token)])


unigram_sentences_filepath = os.path.join(intermediate_directory,
                                          'unigram_sentences_all.txt')



# this takes a while - make the if statement True to execute.
# ADD: TQDM when time permits

if 0 == 1:
    with codecs.open(unigram_sentences_filepath, 'w', encoding='utf_8') as f:
        for sentence in lemmatized_sentence_corpus(event_txt_filepath):
            f.write(sentence + '\n')

# Generate unigram, bigram and trigram sentences

unigram_sentences = LineSentence(unigram_sentences_filepath)

# for unigram_sentence in it.islice(unigram_sentences, 230, 240):
#     print (u' '.join(unigram_sentence))
#     print (u'')

bigram_model_filepath = os.path.join(intermediate_directory, 'bigram_model_all')
bigram_model = Phrases(unigram_sentences)
bigram_model.save(bigram_model_filepath)
bigram_model = Phrases.load(bigram_model_filepath)
bigram_sentences_filepath = os.path.join(intermediate_directory,
                                         'bigram_sentences_all.txt')

print("bigrams done")

# this also takes a while - make the if statement True to execute.
#ADD: TQDM when time permits

if 0 == 1:
    with codecs.open(bigram_sentences_filepath, 'w', encoding='utf_8') as f:
        for unigram_sentence in unigram_sentences:
            bigram_sentence = u' '.join(bigram_model[unigram_sentence])
            f.write(bigram_sentence + '\n')

bigram_sentences = LineSentence(bigram_sentences_filepath)

#Print these if you want to:
for bigram_sentence in it.islice(bigram_sentences, 230, 240):
    print (u' '.join(bigram_sentence))
    print (u'')

trigram_model_filepath = os.path.join(intermediate_directory, 'trigram_model_all')

# ... and also time consuming - make the if statement True
# if you want to execute modeling yourself.
if 1 == 1:
    trigram_model = Phrases(bigram_sentences)
    trigram_model.save(trigram_model_filepath)
    
# load the finished model from disk
trigram_model = Phrases.load(trigram_model_filepath)

trigram_sentences_filepath = os.path.join(intermediate_directory, 
                                            'trigram_sentences_all.txt')


# this is a bit time consuming - make the if statement True
# if you want to execute data prep yourself.
if 0 == 1:
    with codecs.open(trigram_sentences_filepath, 'w', encoding='utf_8') as f:
        for bigram_sentence in bigram_sentences:
            trigram_sentence = u' '.join(trigram_model[bigram_sentence])
            f.write(trigram_sentence + '\n')

trigram_sentences = LineSentence(trigram_sentences_filepath)

# for trigram_sentence in it.islice(trigram_sentences, 230, 240):
#     print (u' '.join(trigram_sentence))
#     print (u'')

trigram_reviews_filepath = os.path.join(intermediate_directory, 'trigram_transformed_reviews_all.txt')


if 1 == 1:
    with codecs.open(trigram_reviews_filepath, 'w', encoding='utf_8') as f:
        for parsed_review in nlp.pipe(line_review(event_txt_filepath),
                                      batch_size=10000, n_threads=4):
            
            # lemmatize the text, removing punctuation and whitespace
            unigram_review = [token.lemma_ for token in parsed_review
                              if not punct_space(token)]
            
            # apply the first-order and second-order phrase models
            bigram_review = bigram_model[unigram_review]
            trigram_review = trigram_model[bigram_review]

            # remove any remaining stopwords
            trigram_review = [term for term in trigram_review
                              if term not in spacy_stopwords]
            
            # write the transformed review as a line in the new file
            trigram_review = u' '.join(trigram_review)
            f.write(trigram_review + '\n')
 
# print (u'Original:' + u'\n')

for review in it.islice(line_review(event_txt_filepath), 11, 12):
    print (review)

# print (u'----' + u'\n')
# print (u'Transformed:' + u'\n')

with codecs.open(event_txt_filepath, encoding='utf_8') as f:
    for review in it.islice(f, 11, 12):
        print (review)

trigram_dictionary_filepath = os.path.join(intermediate_directory,
                                           'trigram_dict_all.dict')

print("done")

if 1 == 1:

    trigram_reviews = LineSentence(trigram_reviews_filepath)

    # learn the dictionary by iterating over all of the reviews
    trigram_dictionary = Dictionary(trigram_reviews)
    
    # filter tokens that are very rare or too common from
    # the dictionary (filter_extremes) and reassign integer ids (compactify)
    trigram_dictionary.filter_extremes(no_below=10, no_above=0.4)
    trigram_dictionary.compactify()

    trigram_dictionary.save(trigram_dictionary_filepath)
    
# load the finished dictionary from disk
trigram_dictionary = Dictionary.load(trigram_dictionary_filepath)

trigram_bow_filepath = os.path.join(intermediate_directory,
                                    'trigram_bow_corpus_all.mm')


def trigram_bow_generator(filepath):
    """
    generator function to read reviews from a file
    and yield a bag-of-words representation
    """
    
    for review in LineSentence(filepath):
        yield trigram_dictionary.doc2bow(review)

if 1 == 1:
    # generate bag-of-words representations for
    # all reviews and save them as a matrix
    MmCorpus.serialize(trigram_bow_filepath,
                       trigram_bow_generator(trigram_reviews_filepath))
    
# load the finished bag-of-words corpus from disk
trigram_bow_corpus = MmCorpus(trigram_bow_filepath)

lda_model_filepath = os.path.join(intermediate_directory, 'lda_model_all')



if 1 == 1:

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        
        # workers => sets the parallelism, and should be
        # set to your number of physical cores minus one
        lda = LdaMulticore(trigram_bow_corpus,
                           num_topics=6,
                           id2word=trigram_dictionary,
                           workers=3)
    
    lda.save(lda_model_filepath)
    
# load the finished LDA model from disk
lda = LdaMulticore.load(lda_model_filepath)

def explore_topic(topic_number, topn=6):
    """
    accept a user-supplied topic number and
    print out a formatted list of the top terms
    """
        
    print (u'{:20} {}'.format(u'term', u'frequency') + u'\n')

    for term, frequency in lda.show_topic(topic_number, topn=25):
        print (u'{:20} {:.3f}'.format(term, round(frequency, 3)))

explore_topic(topic_number=0)

print("done")





# =========from earlier =========
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