import struct
from pydub import AudioSegment


def readaudio(path,format='mp3'):
    sound = AudioSegment.from_file(path,format=format)
    raw=sound.raw_data


def writeaudio(path,data,frame_rate=44100,channels=2,sample_width=2,format='mp3'):
    pass