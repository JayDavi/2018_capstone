import numpy
from numpy import array
import pandas
import gensim
import csv
from gensim.models import word2vec
from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten, Dropout
from keras.layers.embeddings import Embedding
from keras.wrappers.scikit_learn import KerasClassifier
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

path = 'Article_Bodies/fullBody.csv'
w2vPath = 'Article_Bodies/vec/model.csv'
mpath = 'Model/'
# fix random seed for reproducibility
print('start....')

seed = 7
numpy.random.seed(seed)

# load dataset
#Get articles
dataframe = pandas.read_csv(path)
print('-'*91)
# split into input (X) and output (Y) variables
X = dataframe['Body']
Y = dataframe['Stance'] # Labels
for n,b in enumerate(X):
    if len(str(b)) < 20:
        del X[n]
        del Y[n]

# prepare tokenizer
t = Tokenizer()
t.fit_on_texts(X)
vocab_size = len(t.word_index) + 1

# integer encode the documents
print('integer encoding docs......')
encoded_docs = t.texts_to_sequences(X)


# pad documents to a max length of 300 words
max_length = 300
padded_docs = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
print('loading whole emmbeding.......')

# load the whole embedding into memory
embeddings_index = dict()
with open(w2vPath, 'r') as f:
    for line in f:
    	values = line.split()
    	word = values[0]
    	coefs = numpy.asarray(values[1:])
    	embeddings_index[word] = coefs
print('Loaded %s word vectors.' % len(embeddings_index))
# create a weight matrix for words in training docs
embedding_matrix = numpy.zeros((vocab_size, 300))
for word, i in t.word_index.items():
	embedding_vector = embeddings_index.get(word)
	if embedding_vector is not None:
		embedding_matrix[i] = embedding_vector

# baseline model
def create_baseline():
	# create model
    model = Sequential()
    model.add(Embedding(vocab_size, max_length, weights=[embedding_matrix], input_length=300))
    # model.add(Dense(300, input_shape=300, kernel_initializer='normal', activation='relu'))
    # model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
    model.add(Conv1D(64, 3, padding='same'))
    model.add(Conv1D(32, 3, padding='same'))
    model.add(Conv1D(16, 3, padding='same'))
    model.add(Flatten())
    model.add(Dropout(0.2))
    model.add(Dense(180,activation='sigmoid'))
    model.add(Dropout(0.2))
    model.add(Dense(1,activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # serialize model to JSON
    model_json = model.to_json()
    with open(mpath + "model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    file = mpath + "model.h5"
    model.save_weights(mpath + "model.h5")
    print("Saved model to disk")
    return model

# evaluate model with standardized dataset
print('start Classifier')
estimator = KerasClassifier(build_fn=create_baseline, epochs=10, batch_size=5)
print('start kfold')
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
print('cross val score')
results = cross_val_score(estimator=estimator, X=padded_docs, y=Y, cv=kfold, n_jobs=1)
print("Results: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
print('Done!......')
