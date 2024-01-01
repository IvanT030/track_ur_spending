import pyaudio
import wave
import speech_recognition as sr
import openai
import io
import sys
from datetime import datetime


current_datetime = datetime.now()
openai.api_key = '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'
magicword = f"。以上文字是一個使用者用中文說出的花費行為文字，現在請依照此文字判斷是不是可以作為記帳的的用途，如果不相關或是沒有金額或是金額為0，僅輸出:抱歉我聽不懂，麻煩重講一次，若可以則依照以下格是輸出給我:[]年[]月[]日在[]花[]元，[]的部分請依照以下規則填寫，品項上花費請在以下中分類:餐飲、生活、娛樂、交通、投資、醫療、學習、其他，如果未提供時間或提供時間不足就以現在時間補滿，現在時間為{current_datetime.year}年{current_datetime.month}月{current_datetime.day}日。"

speech_to_text = sr.Recognizer()
response_text = ''

while response_text.find("抱歉我聽不懂") != -1 or response_text == "":

    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()
    print("start recording...")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    wf = wave.open("output.wav", 'wb')  # 將初始化移到迴圈外部

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    frames = []
    seconds = 5

    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)

    print("recording stopped")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf.writeframes(b''.join(frames))
    wf.close()
        
    with sr.AudioFile("output.wav") as source:
        audio = speech_to_text.record(source)
        text = speech_to_text.recognize_google(audio, language='zh-TW')
        print(text)
        text += magicword
        model_engine = "text-davinci-003"
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=text,
            max_tokens=128,
            temperature=0.5
        )
        response_text = response['choices'][0]['text']
        print(response_text)