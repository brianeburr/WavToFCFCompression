from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
import csv
import cmath

#This file performs compression from wav to FCF file, using scipy fft tool

class wavToFCF: #defines object which can run the compression task
    def __init__(self, wavNumpy, samplerate, fileName):
        self.wavNum = wavNumpy #wavFile from FFTCompressor
        self.fileName = fileName
        self.samplerate = samplerate

    def runFFT(self,sliceArr):
        returnList = [] # format [(freq, amp), (freq, amp) ...]
        yf = fft(sliceArr) #using scipy fft function to convert y values into corresponding fourier transform
        xf = fftfreq(len(sliceArr), 1/self.samplerate)[:len(sliceArr)//2] #x axis for transform, in Hz
        yfAbs = np.abs(yf[0:len(sliceArr)//2]) 
        yfReal = np.real(yfAbs) #want to return real components of fft output
        
        return xf, yfReal

    #FFT function use assissted by https://stackoverflow.com/questions/23377665/python-scipy-fft-wav-files
    def compressToFCF(self):
        lengthOfTimeSlice = float(input("Length of timeslice (s):")) #how short of a time interval to use per slice, smaller interval = larger file size/more detail, can be too small dependent on freq
        numFrequencies = int(input("Number of individual frequencies:")) #how many individual frequencies to measure per slice
        samplesPerSlice = int(lengthOfTimeSlice*self.samplerate)
        myfile = open(self.fileName[:-4] + '.FCF', 'w', newline='') #write to ".FCF"
        writer = csv.writer(myfile)
        writer.writerow([lengthOfTimeSlice]) #first row is timeslice length
        idx = 0
        FCFout = []
        while idx < len(self.wavNum) - samplesPerSlice: #checks for bounds of wavData
            sliceArr = self.wavNum[idx:idx+samplesPerSlice] #subarray of wavData
            xf, yf = self.runFFT(sliceArr) # runs FFT in function

            
            fourierOut = [list(a) for a in zip(yf, xf)]
            fourierOut.sort(reverse=True)
            tempList = [] #for each sliceArr, take top numFrequencies frequencies based on amplitude
            for x in fourierOut[0:numFrequencies]:
                tempList.append(x[0])
                tempList.append(x[1])
            FCFout.append(tempList) #FCFout written to file

            idx += samplesPerSlice
        print(FCFout)
        #writer.writerows(FCFout)
        for fList in FCFout:
            writer.writerow(fList) #write to file
        myfile.close()


        




