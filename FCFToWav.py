import wave
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
import csv
import cmath
import wave
import struct

SAMPLE_RATE = 44100

#This file converts from FCF to wav file, using details held within file, sampling rate will be 44100, 1 channel, etc.

class FCFToWav:

    def __init__(self, filename):
        self.filename = filename

    def saveWav(self, audioData): #function to output to wav file, using python wav tools, audioData is ordered samples
        wavFile = wave.open(self.filename[:-4] + 'convert.wav', 'wb')
        channels = 1
        sampleWidth = 2 # 16 bit audio samples, help from https://stackoverflow.com/questions/33879523/python-how-can-i-generate-a-wav-file-with-beeps
        numFrames = len(audioData)
        comptype = "NONE"
        compname = "not compressed"
        wavFile.setparams( (channels, sampleWidth, SAMPLE_RATE, numFrames, comptype, compname) )
        for sample in audioData:
            wavFile.writeframes(struct.pack('h', int(sample)))

        wavFile.close()



    def decompressToWAV(self):
        FCFfile = open(self.filename, 'r', newline='')
        FCFreader = csv.reader(FCFfile)
        
        FCFrows = []
        for row in FCFreader:
            FCFrows.append(row)
        lengthOfTimeSlice = float(FCFrows.pop(0)[0]) #length of time slice determines how long each segment should be, numsamples, etc
        samplesPerSlice = int(lengthOfTimeSlice*SAMPLE_RATE)

        numFrequencies = len(FCFrows[0])//2
        FCFamps = []
        FCFfreqs = []
        for row in FCFrows: #convert from FCF format to list of lists containing Amplitude and frequency info
            tempAmps = []
            tempFreqs = []
            for x in range(numFrequencies):
                tempAmps.append(row[x])
                tempFreqs.append(row[x+1])
            FCFamps.append(tempAmps)
            FCFfreqs.append(tempFreqs)
        numSlices = len(FCFamps)

        audioData = []
        for x in range(samplesPerSlice*(numSlices-1)):
            ampAtX = 0;
            for i in range(len(FCFamps[0])): # math below is complicated, floor and remainder division for indexing/wave transitioning, cos function takes radians, adjusted to time based on sampling rate
                amplitude = (float(FCFamps[x//samplesPerSlice][i])*((samplesPerSlice-x%samplesPerSlice)/samplesPerSlice)+ float(FCFamps[x//samplesPerSlice+1][i])*((x % samplesPerSlice) / samplesPerSlice ) )/2
                sinusoid = cmath.cos( ( float(FCFfreqs[x//samplesPerSlice][i]) *((samplesPerSlice-x%samplesPerSlice)/samplesPerSlice)+ float(FCFfreqs[x//samplesPerSlice+1][i])*((x%samplesPerSlice)/samplesPerSlice)  )/2  * (2*cmath.pi) * (x/SAMPLE_RATE) )
                ampAtX += amplitude * sinusoid
            audioData.append(ampAtX)
        maxValue = max(np.abs(audioData))
        scalingTo16Bit = 2**15/maxValue
        audioScaled = [int(np.real(ele * scalingTo16Bit)) for ele in audioData] #audioData must be scaled and placed in 16bit format for saving to WAV

        for x in range(len(audioScaled)): #checking 16bit scaling, needs to be refined, necessary for constructive interference of waves
            if audioScaled[x] > 32766:
                audioScaled[x] = 32766
            if audioScaled[x] < -32767:
                audioScaled[x] = -32767
        self.saveWav(audioScaled)



        