import gensim
from gensim.models import word2vec
import logging
from keras.layers import Input, Embedding, merge
from keras.models import Model
import tensorflow as tf
import numpy as np
import urllib
import os
import pandas as pd

file_for = 'Article_Bodies/con2vec_For.csv'
file_against = 'Article_Bodies/con2vec_Against.csv'
path = 'Article_Bodies/vec/'
pathF = 'Article_Bodies/fullBody.csv'
#------------------------------------------------------------------------------
vector_dim = 300

with open(pathF, 'w') as fp:
    f = open(file_for, 'r')
    fp.write(f.read())
    f.close()
    a = open(file_against, 'r')
    fp.write(a.read())
    a.close()

def read_data(filename):
    """Extract the first file enclosed in a zip file as a list of words."""
    dataframe = pd.read_csv(filename)
    data = dataframe['Body']
    d = dataframe['Stance']
    for n,b in enumerate(data):
        if len(str(b)) < 20:
            del data[n]
            del d[n]
    return data

def convert_data_to_index(string_data, wv):
    index_data = []
    for word in string_data:
        if word in wv:
            index_data.append(wv.vocab[word].index)
    return index_data

def gensim_run(file):
    sentences = word2vec.Text8Corpus(file)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = word2vec.Word2Vec(sentences, iter=10, min_count=30, size=300, workers=4)
    w2v = dict(zip(model.wv.index2word, model.wv.syn0))


    str_data = read_data(file)
    index_data = convert_data_to_index(str_data, model.wv)

    # save and reload the model
    model.wv.save_word2vec_format(path + 'model.csv', binary=False)


def create_embedding_matrix(model):
    # convert the wv word vectors into a numpy matrix that is suitable for insertion
    # into our TensorFlow and Keras models
    embedding_matrix = np.zeros((len(model.wv.vocab), vector_dim))
    for i in range(len(model.wv.vocab)):
        embedding_vector = model.wv[model.wv.index2word[i]]
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    return embedding_matrix


if __name__ == "__main__":
    gensim_run(pathF)
