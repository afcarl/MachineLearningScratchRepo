import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from keras.models import load_model
import tensorflow as tf
import sys

def train_model(genre,dir_model,seq_length,epochs,batch_size):
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True)) #check gpu is being used
    
    X = np.load('playlists/%s/X_sl%d.npy'%(genre,seq_length))
    y = np.load('playlists/%s/y_sl%d.npy'%(genre,seq_length))
    
    try:
        model = load_model(dir_model)
        print("successfully loaded previous model, continuing to train")
    except:
        print("generating new model")
        model = Sequential()
        model.add(LSTM(512, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
        model.add(Dropout(0.2))
        model.add(LSTM(512, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(y.shape[1], activation='softmax'))
        
        optimizer = Adam(lr=1e-5, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    print(model.summary())
    checkpoint = ModelCheckpoint(dir_model, monitor='loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]
    model.fit(X, y, epochs=epochs, batch_size=batch_size, callbacks=callbacks_list, validation_split=0.2, verbose=2)
    model.save(dir_model)

if __name__ == '__main__':
    genre = 'country'
    #seq_length = 200
    seq_length = int(sys.argv[1])
    dir_model = 'models/%s_sl%d.h5'%(genre,seq_length)
    
    epochs = 40
    batch_size = 256
    
    train_model(genre,dir_model,seq_length,epochs,batch_size)



