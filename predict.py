# from keras.models import Sequential
# from keras.layers import Dense
from keras.models import model_from_json
from keras.preprocessing.text import Tokenizer
import keras.preprocessing.sequence
import numpy as np

tpath = 'Article_Bodies/test_article2.txt'
lmodel = 'Model/model.json'
lweight = 'Model/model.h5'

print "start......."
# load json and create model
print "loading model....."
json_file = open(lmodel, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(lweight)
print "Loaded model from disk......."

#Read from test file
with open(tpath, "r") as f:
    a = f.read()
    art = a.encode('ascii', 'ignore')

#Turn into numer representation
text = np.array([art])
tk = Tokenizer(
        num_words=300,
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
        lower=True,
        split=" ")
tk.fit_on_texts(text)
seq = keras.preprocessing.sequence.pad_sequences(tk.texts_to_sequences(text), maxlen=300, dtype='int32', padding='pre', truncating='pre', value=0.0)
pred = loaded_model.predict(np.array(seq), steps=10)

#Say For or Against if certain value is returned
v = pred[0][0]
if v < 0.55:
    print 'For = %s \nAgainst = %s' % (v, 1 - v)
else:
    print 'Against = %s \nFor = %s' % (v, 1 - v)
