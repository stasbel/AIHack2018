from nltk.corpus import stopwords
import re
import pandas as pd
import numpy as np

def get_features(text, index):
    stop_words = set(stopwords.words('russian'))
    txt = text.fillna('').str.lower()
    features = {'punct': [],
            'string_len': [],
            'count_nums':[],
            'number_words':[],
            'stop_words':[],
            'not_stop_words':[],
            'larger_than_three':[],
            'exclamation': []}
    for tx in txt:
        tx_p = remove_punct(tx)
        features['punct'].append(get_punct(tx))
        features['string_len'].append(len(tx))
        features['count_nums'].append(get_num(tx))
        features['number_words'].append(len(tx_p.split()))
        features['stop_words'].append(get_stop_words(tx_p, stop_words))
        features['not_stop_words'].append(not_stop_words(tx_p, stop_words))
        features['larger_than_three'].append(words_larger_three(tx_p))
        features['exclamation'].append(exclam(tx))
    return pd.DataFrame(features, index=index, dtype=float)
    
    
def remove_punct(txt):
    return re.sub('[^A-Za-zа-яА-Я ]','', txt)
    
def get_punct(txt):
    return(len(re.findall('[^A-Za-zа-яА-Я0-9 ]', txt)))

def get_num(txt):
    return(len(re.findall('[0-9]', txt)))

def get_stop_words(txt, stop_words):
    return len([word for word in txt.split() if word in stop_words])

def not_stop_words(txt,stop_words):
    return len([word for word in txt.split() if word not in stop_words])

def words_larger_three(txt):
    return len([word for word in txt.split() if len(word)>3])
def exclam(txt):
    if '!' in txt:
        return 1
    else:
        return 0
