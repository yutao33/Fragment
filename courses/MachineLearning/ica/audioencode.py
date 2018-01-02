
import numpy
from scikits.audiolab import flacread, flacwrite
from numpy import abs,max,array

data1,fs1,enc1=flacread('mhh.flac')
data2,fs2,enc2=flacread('lz.flac')
data1=data1[:,0]
data2=data2[:,0]

l=min(len(data1),len(data2))-1

mixed1=0.5*data1[0:l]+0.7*data2[0:l]
mixed2=0.5*data1[0:l]+0.75*data2[0:l]
d=numpy.c_[mixed1,mixed2]
flacwrite(d,'mix.flac',fs1,enc1)