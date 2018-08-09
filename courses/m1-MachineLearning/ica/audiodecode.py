import mdp
import numpy
from mdp import fastica
from scikits.audiolab import flacread, flacwrite
from numpy import abs, max
 
# Load in the stereo file
recording, fs, enc = flacread('mix.flac')


l=len(recording)
a=l*0/8
b=l*8/8-1
recording=recording[a:b]
# Perform FastICA algorithm on the two channels
sources = fastica(recording) 
# node = mdp.nodes.FastICANode()

# 12117935
# [2000000:3000000]
 
# The output levels of this algorithm are arbitrary, so normalize them to 1.0.
sources /= max(abs(sources), axis = 0)
 
# Write back to a file
flacwrite(sources, 'sources.flac', fs, enc)
