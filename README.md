# Real-time-voice-active-detection
 Real time voice active detection

## Method

1. Detect default parameters during a silent period.
2. Calculate the short-term energe(E) of one frame.
3. Calculate the Spectral Flatness Measure(SFM) and the dominant frequency component(F) of the frame.
4. Compare the feature of the frame with the default parameters to figure out whether the voice is active in this frame.
5. Update the default parameters according to the new frame detected. 



## Reference 

Moattar, Mohammad & Homayoonpoor, Mahdi. (2010). A simple but efficient real-time voice activity detection algorithm. European Signal Processing Conference. 