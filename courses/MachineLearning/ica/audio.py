import struct
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
from sklearn.decomposition import FastICA
from mdp import fastica

def readaudio1(path,format='mp3'):
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

def readaudio(path,format='mp3'):
    """
    read an audio
    return numpy.array,frame_rate
    """
    sound = AudioSegment.from_file(path,format=format)
    raw=sound.raw_data
    w=sound.sample_width
    if w==1:
        dtype=np.int8
    elif w==2:
        dtype=np.int16
    elif w==4:
        dtype=np.int32
    else:
        raise Exception("unexcepted sample_width")
    amax=2**(w*8-1)
    col=sound.channels
    row=len(raw)//w//col
    data=np.ndarray([row,col],dtype=dtype,buffer=raw)
    data=data/amax
    return data,sound.frame_rate

def writeaudio(path,data,frame_rate=44100,sample_width=2,format='mp3'):
    """
    write an audio

    """
    w=sample_width
    if w==1:
        dtype=np.int8
    elif w==2:
        dtype=np.int16
    elif w==4:
        dtype=np.int32
    else:
        raise Exception("unexcepted sample_width")
    amax=2**(w*8-1)
    d=dtype(data*amax).tobytes()
    sound = AudioSegment(data=d,sample_width=sample_width,frame_rate=frame_rate,channels=data.shape[1])
    sound.export(out_f=path,format=format)

def test1():
    data,fr=readaudio(r"C:\Users\yutao\Downloads\lz.mp3")
    data=data[4444:len(data)//2]
    writeaudio(r"C:\Users\yutao\Downloads\out.mp3",data)

def test2():
    data,fr=readaudio(r"C:\Users\yutao\Downloads\lz.mp3")
    plt.plot(data)
    plt.show()


def mix():
    data1,fs1=readaudio(r"C:\Users\yutao\Downloads\lz.mp3")
    data2,fs2=readaudio(r"C:\Users\yutao\Downloads\mhh.mp3")
    assert fs1==fs2
    data1=data1[:,0]
    data2=data2[:,0]
    l=min(len(data1),len(data2))-1
    mixed1=0.4*data1[0:l]+0.4*data2[0:l]
    mixed2=0.4*data1[0:l]+0.3*data2[0:l]
    #mixed1=data1[0:l]
    #mixed2=data2[0:l]
    print(mixed1.shape)
    print(mixed2.shape)
    d=np.c_[mixed1,mixed2]
    writeaudio(r"C:\Users\yutao\Downloads\out.wav",d,format='wav')


def unmix():
    data,fs=readaudio(r"C:\Users\yutao\Downloads\out.wav")
    # d=FastICA().fit(data).transform(data)
    print(data.shape)
    d=fastica(data)
    d /= np.max(abs(d), axis = 0)
    writeaudio(r"C:\Users\yutao\Downloads\out1.wav",d,format='wav')

def unmix_1():
    data,fs=readaudio(r"C:\Users\yutao\Downloads\mhh.mp3")
    d=fastica(data)
    d /= np.max(abs(d), axis = 0)
    writeaudio(r"C:\Users\yutao\Downloads\mhh_unmix.wav",d,format='wav')

def unmix_2():
    data,fs=readaudio(r"C:\Users\yutao\Downloads\bbcenglish.mp3")
    d=fastica(data)
    d /= np.max(abs(d), axis = 0)
    writeaudio(r"C:\Users\yutao\Downloads\bbcenglish_unmix.wav",d,format='wav')


def sin_rand():
    x=np.linspace(0,30,1000)
    print(x)
    y_sin=np.sin(x)
    noise1=np.random.normal(size=y_sin.shape)
    noise2=np.random.normal(size=y_sin.shape)
    y1=y_sin+0.5*noise1
    y2=y_sin+0.5*noise2
    plt.subplot(211)
    plt.plot(x,y1)
    plt.plot(x,y2)
    y=np.c_[y1,y2]
    ica=FastICA()
    yy=ica.fit(y).transform(y)
    print(ica.mixing_)
    plt.subplot(212)
    plt.plot(x,yy)
    plt.show()

def test3():
    data,fr=readaudio(r"C:\Users\yutao\Downloads\bbcenglish.mp3")
    data=data
    ica=FastICA()
    dd=ica.fit(data).transform(data)
    print(ica.mixing_)
    #plt.plot(data)
    # plt.plot(dd)
    a=np.int32(np.linspace(0,len(data)-2,10000))
    plt.scatter(data[a,0],data[a,1],s=1)
    plt.show()

def test4():
    data,fs=readaudio(r"C:\Users\yutao\Downloads\wangningmei.mp3")
    #d=fastica(data)
    d=data.dot(np.array([[1,1],[1,-1]]))
    d /= np.max(abs(d), axis = 0)
    writeaudio(r"C:\Users\yutao\Downloads\wangningmei_unmix_manual.wav",d,format='wav')


if __name__=="__main__":
    test3()
