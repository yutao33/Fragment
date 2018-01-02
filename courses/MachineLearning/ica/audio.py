import struct
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
import ctypes

def readaudio(path,format='mp3'):
    """
    read an audio
    return numpy.array,frame_rate
    """
    sound = AudioSegment.from_file(path,format=format)
    raw=sound.raw_data
    w=sound.sample_width
    if w==1:
        astr="b"
    elif w==2:
        astr="h"
    elif w==4:
        astr="i"
    else:
        raise Exception("unexcepted sample_width")
    amax=2**(w*8-1)
    col=sound.channels
    row=len(raw)//w//col
    data=np.zeros([row,col])
    for r in range(0,row):
        for c in range(0,col):
            k=struct.unpack_from(astr,raw,(r*col+c)*w)
            # k=ctypes.c_short.from_buffer(raw,(r*col+c)*w).value
            data[r,c]=k[0]/amax
    return data,sound.frame_rate


def writeaudio(path,data,frame_rate=44100,sample_width=2,format='mp3'):
    """
    write an audio

    """
    sound = AudioSegment()

def test1():
    data,fr=readaudio(r"C:\Users\yutao\Downloads\lz.mp3")
    plt.plot(data[44444:55555])
    plt.show()

if __name__=="__main__":
    test1()