import pyaudio
import tkinter as tk
import numpy as np 
import tqdm

from voice_detective_helper import ActiveVoiceHelper


class ActiveVoiceDetector():
    def __init__(self, 
                chunk=1200,
                channels=1,
                rate=44100,
                energe_prime_thresh=60000,
                f_prime_thresh=185,
                sf_prime_thresh=5):
        # number of sampling points of each frame
        self.CHUNK = chunk
        # bit depth
        self.FORMAT = pyaudio.paInt16
        # number of the channels
        self.CHANNELS = channels
        # sampling rate
        self.RATE = rate
        # time of recording
        self.RECORD_SECONDS = 5
        # file name of the .wav file
        self.WAVE_OUTPUT_FILENAME = "cache.wav"

        # prime threshold
        self.ENERGE_PRIME_THRESH = energe_prime_thresh
        self.F_PRIME_THRESH = f_prime_thresh #Hz
        self.SF_PRIME_THRESH = sf_prime_thresh

        # successive frame number
        self.SUCCESSIVE_SILENCE_FRAME_NUMBER = 10
        self.SUCCESSIVE_ACTIVE_FRAME_NUMBER = 5

        # threshold
        self.energe_thresh = 40
        self.f_thresh = 185
        self.sf_thresh = 5

        # min value
        self.min_e = 1000000
        self.min_f = 1000000
        self.min_sf = 1000000

        # help value
        self.frames = []
        self.silence_counter = 0

        # audio stream
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        # a set of function for calculation
        self.helper = ActiveVoiceHelper()

    def _one_frame_value(self, audio_data):
        energe = self.helper.calculate_frame_energy(audio_data)
        f = self.helper.calculate_dominant_frequncy(audio_data, self.RATE)
        sfm = self.helper.calculate_smf(audio_data)
        # print(energe)
        return energe, f, sfm

    def _silence_min_value(self, audio_data):
        e, f, sf = self._one_frame_value(audio_data)
        if self.min_e > e:
            self.min_e = e
        if self.min_f > f:
            self.min_f = f
        if self.min_sf > sf:
            self.min_sf = sf

    def _frame_judge(self, audio_data):
        e, f, sf = self._one_frame_value(audio_data)
        counter = 0
        if (e - self.min_e) > self.energe_thresh:
            counter += 1
        if (f - self.min_f) > self.f_thresh:
            counter += 1
        if (sf - self.min_sf) > self.sf_thresh:
            counter += 1

        # print([e - self.min_e])
        active = False

        # silence case
        if counter == 0:
            self.silence_counter += 1
            self.min_e = ((self.silence_counter * self.min_e) + e) / (self.silence_counter + 1)
            self.energe_thresh = self.ENERGE_PRIME_THRESH * np.log10(self.min_e)
        # active case
        else:
            active = True

        if active == True:
            return True
        else:
            return False

    def _audio_read(self):
        data = self.stream.read(self.CHUNK)
        string_data = np.frombuffer(data, dtype=np.short)
        string_data = string_data / 10000
        return string_data

    def vad(self):
        # first 30 silence frames for initialization
        print("Silence Initializing")
        for _ in tqdm.tqdm(range(100)):
            self._silence_min_value(self._audio_read())

        self.energe_thresh = self.ENERGE_PRIME_THRESH * np.log10(self.min_e)
        self.f_thresh = self.F_PRIME_THRESH
        self.sf_thresh = self.SF_PRIME_THRESH

        print(self.energe_thresh)
        print(self.f_thresh)
        print(self.sf_thresh)

        print(self.min_e)
        print(self.min_f)

        active_frame_number = 0
        silence_frame_number = 0


        active_run = False

        while(True):
            state = self._frame_judge(self._audio_read())

            if state and not active_run:
                active_frame_number += 1
                silence_frame_number = 0
            elif not state and active_run:
                silence_frame_number += 1
                active_frame_number = 0

            if active_frame_number == self.SUCCESSIVE_ACTIVE_FRAME_NUMBER and not active_run:
                active_run = True
                print("active start")
            
            if silence_frame_number == self.SUCCESSIVE_SILENCE_FRAME_NUMBER and active_run:
                active_run = False
                print("active end")
            