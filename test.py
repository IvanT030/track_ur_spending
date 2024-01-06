import tkinter as tk
import pyaudio
import wave
import threading

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.frames_per_buffer = 3200
        self.pyaudio_instance = pyaudio.PyAudio()

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.stream = self.pyaudio_instance.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.frames_per_buffer
        )
        self.recording_thread = threading.Thread(target=self.record)
        self.recording_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.recording_thread.join()

        with wave.open("recording.wav", 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.pyaudio_instance.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

    def record(self):
        while self.is_recording:
            data = self.stream.read(self.frames_per_buffer)
            self.frames.append(data)

# Tkinter界面
def toggle_recording():
    if not recorder.is_recording:
        recorder.start_recording()
        button.config(text='Stop Recording')
    else:
        recorder.stop_recording()
        button.config(text='Start Recording')

root = tk.Tk()
recorder = AudioRecorder()
button = tk.Button(root, text='Start Recording', command=toggle_recording)
button.pack()

root.mainloop()

