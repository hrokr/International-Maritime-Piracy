

import os
import codecs

import spacy
import pandas as pd
import itertools as it
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence

nlp = spacy.load('en')

data_directory = os.path.join('..', 'data')

piracy_filepath = os.path.join(data_directory, 'mungedASAM.json')

with codecs.open(piracy_filepath, encoding='utf_8') as f:
    firstpiracyrecord = f.readline() 

print (firstpiracyrecord)

import json

events = [i for i in range(7843)]
event_ids = set(events)

with codecs.open(piracy_filepath, encoding='utf_8') as f:
     for event_json in f:
        event = json.loads(event_json)
        for item in event:         
           event_descriptions.add(item[u'description'])

# turn priacy_ids into a frozenset, as we don't need to change it anymore
priacy_ids = frozenset(priacy_ids)


intermediate_directory = os.path.join('..', 'intermediate')

record_txt_filepath = os.path.join(intermediate_directory,
                                   'record_text_all.txt')

                                   

# this is a bit time consuming - make the if statement True
# if you want to execute data prep yourself.
if 0 == 1:
    
    record_count = 0
    with codecs.open(record_txt_filepath, 'w', encoding='utf_8') as record_txt_file:
        with codecs.open(record_json_filepath, encoding='utf_8') as record_json_file:
            for record_json in record_json_file:
                record = json.loads(record_json)

            
    print (u'''Text from {:,} priacy records
              written to the new txt file.'''.format(record_count))
    
else:
    
    with codecs.open(record_txt_filepath, encoding='utf_8') as record_txt_file:
        for record_count, line in enumerate(record_txt_file):
            pass
        
    print (u'Text from {:,} priacy records in the txt file.'.format(record_count + 1))

    with codecs.open(record_txt_filepath, encoding='utf_8') as f:
        sample_record = list(it.islice(f, 8, 9))[0]
        sample_record = sample_record.replace('\\n', '\n')
        
print (sample_record)


token_attributes = [(token.orth_,
                     token.prob,
                     token.is_stop,
                     token.is_punct,
                     token.is_space,
                     token.like_num,
                     token.is_oov)
                    for token in parsed_record]

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
                                               
df