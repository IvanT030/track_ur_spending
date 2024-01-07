import tkinter as tk
import sounddevice as sd
import numpy as np
import threading
import wave

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.audio_data = []
        self.samplerate = 44100  # 樣本率
        self.channels = 1  # 單聲道

    def start_recording(self):
        self.audio_data = []
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self.record)
        self.recording_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.recording_thread.join()

    def record(self):
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self.callback):
            while self.is_recording:
                sd.sleep(100)

    def callback(self, indata, frames, time, status):
        self.audio_data.append(indata.copy())

    def save(self, filename):
        if self.audio_data:
            audio_data_np = np.concatenate(self.audio_data, axis=0)
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 16位
                wf.setframerate(self.samplerate)
                wf.writeframes(audio_data_np.tobytes())

# Tkinter界面
def toggle_recording():
    if not recorder.is_recording:
        recorder.start_recording()
        button.config(text='Stop Recording')
    else:
        recorder.stop_recording()
        recorder.save("recording.wav")
        button.config(text='Start Recording')

root = tk.Tk()
recorder = AudioRecorder()
button = tk.Button(root, text='Start Recording', command=toggle_recording)
button.pack()

root.mainloop()
