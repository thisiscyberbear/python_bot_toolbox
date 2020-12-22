import soundcard as sc
import numpy as np
from scipy.io.wavfile import write, read

# Displays the speakers on the system
def getSpeakers():
	speakers = sc.all_speakers()
	print(speakers)
	return speakers
	
# Displays the default speaker on the system
def getDefaultSpeaker():
	default_speaker = sc.default_speaker()
	print(default_speaker)
	return default_speaker

# Displays the microphones on the system
def getDefaultSpeaker():
	mics = sc.all_microphones()
	print(mics)
	return mics
	
# Displays the default microphone on the system
def getDefaultMic():
	default_mic = sc.default_microphone()
	print(default_mic)
	return default_mic
 
# Function to record the audio from the default microphone for a defined duration in seconds
# @duration: Recording duration in seconds
def recordMic_func(duration = 5, filename = 'output.wav'): 
	default_mic = sc.default_microphone()
	# Record for defined time
	data = default_mic.record(samplerate=48000, numframes=48000*duration)
	scaled = np.int16(data/np.max(np.abs(data)) * 32767)
	write(filename, 48000, scaled)
	
# Function to play audio
# @filename: Filename/-path of the playback file
def playAudio_func(filename): 
	default_speaker = sc.default_speaker()
	
	# Read input file 
	samplerate, data = read(filename)
	
	# Playback of the input file 
	default_speaker.play(data/np.max(data), samplerate=samplerate)
