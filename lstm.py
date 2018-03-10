import numpy as np
import pandas as pd

from keras.models import Model
from keras.preprocessing import text, sequence
from keras.layers import Dense, Embedding, Input
from sklearn.base import BaseEstimator, TransformerMixin
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import LSTM, Bidirectional, GlobalMaxPool1D, Dropout


class KTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self, num_words=1000, max_len=100):
        self.num_words = num_words
        self.max_len = max_len
        
        self._tok = text.Tokenizer(self.num_words)
    
    def fit(self, X):
        self._tok.fit_on_texts(list(X.fillna('CVxTz')))
        return self
    
    def transform(self, X):
        return sequence.pad_sequences(self._tok.texts_to_sequences(list(X.fillna('CVxTz'))), self.max_len)


def get_score(test, weights='weights_base_1.best.hdf5', max_len=100, 
              max_features=1000, in_LSTM=50, dense1=16,
              dense2=1, dropout1=0.1, dropout2=0.1):
    model = get_model(max_len, max_features, in_LSTM, dense1, dense2, dropout1, dropout2)
    model.load_weights(weights)
    return model.predict(test)


def get_model(maxlen, max_features, in_LSTM, dense1, dense2, dropout1, dropout2):
    embed_size = 128
    inp = Input(shape=(maxlen, ))
    x = Embedding(max_features, embed_size)(inp)
    x = Bidirectional(LSTM(in_LSTM, return_sequences=True))(x)
    x = GlobalMaxPool1D()(x)
    x = Dropout(dropout1)(x)
    x = Dense(dense1, activation="relu")(x)
    x = Dropout(dropout2)(x)
    x = Dense(dense2, activation="sigmoid")(x)
    model = Model(inputs=inp, outputs=x)
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model