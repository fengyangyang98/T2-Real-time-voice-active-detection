import numpy as np

class ActiveVoiceHelper():
    def _geometric_mean(self, t):
        total = 1
        n = len(t)
        for num in t:
            total *= np.power(num, 1/n)
        return total

    def _calculate_amplitude(self, audio_data_frame):
        data_ampl = np.abs(np.fft.fft(audio_data_frame))
        data_ampl = data_ampl[1:]
        return data_ampl

    def _calculate_frequencies(self, audio_data, rate):
        data_freq = np.fft.fftfreq(len(audio_data),1.0/rate)
        data_freq = data_freq[1:]
        return data_freq    

    def calculate_frame_energy(self, audio_data_frame):
        data_amplitude = self._calculate_amplitude(audio_data_frame)
        data_energy = data_amplitude ** 2
        return sum(data_energy)

    def calculate_dominant_frequncy(self, audio_data_frame, rate):
        return max(self._calculate_frequencies(audio_data_frame, rate))

    def calculate_smf(self, audio_data_frame):
        data_amplitude = self._calculate_amplitude(audio_data_frame)
        arithmetic_mean = np.mean(data_amplitude)
        geometric_mean = self._geometric_mean(data_amplitude)
        smf = 10 * np.log10(geometric_mean / arithmetic_mean)
        return smf