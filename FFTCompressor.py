from scipy.fftpack import fft
from scipy.io import wavfile
import matplotlib.pyplot as plt
from FCFToWav import FCFToWav
import wavToFCF
import FCFToWav

#Project to compress standard wav files into "FCF" files, which stores small timeslices of sound as the dominant frequencies
#Menu runs either compression task or decompression, prompts user for filenames
#FCF takes form of csv file, .wav opened best with Audacity or other audio tool

userChoice = ""
while userChoice != "Q":
    print("FFT Wave file compressor:")
    print("1. Convert WAV file to FCF")
    print("2. Convert FCF to WAV")
    print("Q. Quit")
    userChoice = input("Choose option\n")

    match userChoice:
        case "1": #runs compresssion
            fileName = input("File Name (.wav)? full path or relative\n")
            samplerate, data = wavfile.read(fileName)
            FCFConverter = wavToFCF.wavToFCF(data, samplerate, fileName)
            FCFConverter.compressToFCF()
            print("Converted! FCF file located in project directory")
            
        case "2": #runs decompression
            filename = input("File name (.FCF)? full path or relative\n")
            WAVConverter = FCFToWav.FCFToWav(filename)
            WAVConverter.decompressToWAV()
            print("Converted! Wav file located in project directory")

        case "Q":
            break


