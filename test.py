# -*- coding: utf-8 -*-
import pyaudio
import wave
import speech_recognition as sr
import openai
import sys
from datetime import datetime
import asyncio

current_datetime = datetime.now()
keys = ['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','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']
max_keys = 1
avliable_key = 0
magicword = f"。以上文字是一個使用者用中文說出的花費行為文字，現在請依照此文字判斷是不是可以作為記帳的的用途，如果不相關或是沒有金額或是金額為0，僅輸出:抱歉我聽不懂，麻煩重講一次，若可以則依照以下格是輸出給我:[]年[]月[]日在[]花[]元，[]的部分請依照以下規則填寫，品項上花費請在以下中分類:餐飲、生活、娛樂、交通、投資、醫療、學習、其他，如果未提供時間或提供時間不足就以現在時間補滿，現在時間為{current_datetime.year}年{current_datetime.month}月{current_datetime.day}日。"

speech_to_text = sr.Recognizer()
avliable_key = 0
response_text = ''
response_text_lock = asyncio.Lock()  # 新增 Lock
sys.stdout.encoding
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
seconds = 5

p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

def recordAudio():
    print("start recording...")
    
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    for _ in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        wf.writeframes(data)
        
    wf.close()

async def sendrequest():
    with sr.AudioFile("output.wav") as source:
        audio = speech_to_text.record(source)
        try:
            text = speech_to_text.recognize_google(audio, language='zh-TW')
        except sr.exceptions.UnknownValueError as e:
            print("There is an Error")
            return
        print(text)
        text += magicword
        model_engine = "text-davinci-003"
        async with response_text_lock:  # 使用 Lock 保護 response_text 的操作
            openai.api_key = keys[avliable_key]
            try:
                response = openai.Completion.create(
                    model='text-davinci-003',
                    prompt=text,
                    max_tokens=128,
                    temperature=0.5
                )
            except openai.error.RateLimitError as e:
                if avliable_key == max_keys:
                    avliable_key = 0
                else :
                    avliable_key += 1
                print("RateLimitError")
            response_text = response['choices'][0]['text']
            print(response_text)


async def main():
    while response_text.find("抱歉我聽不懂") != -1 or response_text == "":
        recordAudio()
        await sendrequest()

asyncio.run(main())