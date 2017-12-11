#https://github.com/vlraik/word-level-rnn-keras/blob/master/lstm_text_generation.py

import numpy as np
import glob
import sys
from keras.utils import np_utils
from process_lyrics import *

def main(genre,n_songs,seq_length,word_or_character):
    
    # get song lyrics
    dir_lyrics = 'playlists/%s/'%genre
    files = glob.glob('%s*.txt'%dir_lyrics)[0:n_songs]
    songs, n_songs = [], len(files)
    for i,f in enumerate(files):
        songs.append(process_song(f, word_or_character))

    # get char/int mappings
    if word_or_character == 'character':
        data = sorted(list(set(' '.join(songs))))
    elif word_or_character == 'word':
        data = []
        for s in songs:
            data += s
        data = set(data)    #gets unique values
    n_data = len(data)      #total number of chars/words
    char_to_int = dict((c, i) for i, c in enumerate(data))
    int_to_char = dict((i, c) for i, c in enumerate(data))
    np.save('%sancillary_%s.npy'%(dir_lyrics,word_or_character),
            [char_to_int,int_to_char,n_data])

    # get data arrays for training LSTMs
    for sl in seq_length:
        dataX, dataY = [], []
        for i in range(n_songs):
            lyric = songs[i]
            for j in range(0,len(lyric)-sl):
                seq_in = lyric[j:j + sl]
                seq_out = lyric[j + sl]
                dataX.append([char_to_int[char] for char in seq_in])
                dataY.append(char_to_int[seq_out])
        n_patterns = len(dataX)
        print("Total Patterns: ", n_patterns)

        # prepare
        X = np.reshape(dataX, (n_patterns,sl,1))    # reshape X:[samples,time steps,features]
        X = X / float(n_data)                       # normalize
        y = np_utils.to_categorical(dataY)          # 1-hot encode the output variable
        print(y.shape, n_data)

        # save data
        np.save('%sX_sl%d_%s.npy'%(dir_lyrics,sl,word_or_character),X)
        np.save('%sy_sl%d_%s.npy'%(dir_lyrics,sl,word_or_character),y)


if __name__ == '__main__':
    n_songs = -1
    #seq_length = [25,50,75,100,125,150,175,200]
    seq_length = [3,6,9,12,15]
    word_or_character = 'word'
    
    #genre = sys.argv[1]
    genre = 'country'

    main(genre,n_songs,seq_length,word_or_character)
