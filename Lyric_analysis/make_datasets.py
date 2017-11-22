#https://github.com/vlraik/word-level-rnn-keras/blob/master/lstm_text_generation.py

import numpy as np
import glob
import sys
import unidecode
from keras.utils import np_utils
from clean_lyrics import *

def process_song(song_dir, word_or_character):
    song = open(song_dir,'r',encoding='utf-8').read().lower()
    song = unidecode.unidecode(unicodetoascii(song, word_or_character))
    if word_or_character == 'word':
        return song.split()
    return song

def main(genre,n_songs,seq_length,word_or_character):
    dir_lyrics = 'playlists/%s/'%genre
    files = glob.glob('%s*.txt'%dir_lyrics)[0:n_songs]
    songs, n_songs = [], len(files)
    for i,f in enumerate(files):
        songs.append(process_song(f, word_or_character))

    if word_or_character == 'character':
        data = sorted(list(set(' '.join(songs))))
    elif word_or_character == 'word':
        data = []
        for s in songs:
            data += s

    n_chars = len(data)
    char_to_int = dict((c, i) for i, c in enumerate(data))
    int_to_char = dict((i, c) for i, c in enumerate(data))

    dataX, dataY = [], []
    for i in range(n_songs):
        lyric = songs[i]
        for j in range(0,len(lyric)-seq_length, 1):
            seq_in = lyric[j:j + seq_length]
            seq_out = lyric[j + seq_length]
            #print(seq_in, seq_out)
            dataX.append([char_to_int[char] for char in seq_in])
            dataY.append(char_to_int[seq_out])
    n_patterns = len(dataX)
    print("Total Patterns: ", n_patterns)

    # prepare
    X = np.reshape(dataX, (n_patterns,seq_length,1))    # reshape X:[samples,time steps,features]
    X = X / float(n_chars)                              # normalize
    y = np_utils.to_categorical(dataY)                  # 1-hot encode the output variable
    print(y.shape)

    # save data
    np.save('%sX_sl%d.npy'%(dir_lyrics,seq_length),X)
    np.save('%sy_sl%d.npy'%(dir_lyrics,seq_length),y)
    np.save('%schar_to_int.npy'%dir_lyrics,char_to_int)
    np.save('%sint_to_char.npy'%dir_lyrics,int_to_char)

#    # text generation
#    seed = np.random.randint(0, n_songs)
#    ini = songs[seed][0:seq_length]     #set initial = start of a song
#    pattern = [char_to_int[v] for v in list(ini)]
#    print("Song:%s"%files[seed])
#    print("Seed:%s"%ini)
#    # generate characters
#    for i in range(100):
#        x = np.reshape(pattern, (1, len(pattern), 1))
#        x = x / float(n_chars)
#        pred = model.predict(x, verbose=0)
#        #index = np.argmax(pred)
#        index = np.random.choice(len(pred[0]), p=pred[0])
#        result = int_to_char[index]
#        seq_in = [int_to_char[value] for value in pattern]
#        sys.stdout.write(result)
#        pattern.append(index)
#        pattern = pattern[1:len(pattern)]
#    print("\nDone.")

if __name__ == '__main__':
    n_songs = -1
    seq_length = 200
    word_or_character = 'character'
    
    #genre = sys.argv[1]
    genre = 'country'

    main(genre,n_songs,seq_length,word_or_character)