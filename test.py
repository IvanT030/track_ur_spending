# -*- coding: utf-8 -*-
import pyaudio
import wave
import speech_recognition as sr
import openai
import sys
from datetime import datetime
import asyncio

current_datetime = datetime.now()
keys = ['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', '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']
max_keys = 1
avliable_key = 0
magicword = f"""。以上文字是一個使用者用花費行為文字，依照此文字判斷是不是可以作為記帳的的用途，
        如果不相關或是沒有金額或是金額為0，僅輸出:抱歉我聽不懂，麻煩重講一次，若可以則依照以下規則輸出給我，
        在文字中的品項花費請在以下中分類:餐飲、生活、娛樂、交通、投資、醫療、學習、其他，並輸出'品項：哪個分類'，
        再來今天的時間是{current_datetime.year}年{current_datetime.month}月{current_datetime.day}日，
        請在花費行為文字中提取年月日，如果無法提取所有的年月日，就依照我剛剛給你的時間推算，並輸出'日期:?年?月?日'
        ，比如說文字中提到前年，則輸出{current_datetime.year - 2}年{current_datetime.month}月{current_datetime.day}日，
        最後是在花費行為文字提取金錢，並輸出'花費:?元'。給你一個輸出格式的範例，'品項: 娛樂，時間: 2023年12月6日，花費: 300元' 
        """

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
    global avliable_key
    global response_text
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
            while response_text == "":
                print("using " + str(avliable_key) + " key")
                openai.api_key = keys[avliable_key]
                try:
                    response = openai.Completion.create(
                        model='text-davinci-003',
                        prompt=text,
                        max_tokens=128,
                        temperature=0.5
                    )
                    response_text = response['choices'][0]['text']
                except openai.error.RateLimitError as e:
                    if avliable_key == max_keys:
                        avliable_key = 0
                    else :
                        avliable_key += 1
                    print("RateLimitError")
                
async def main():
    global response_text
    while response_text.find("抱歉我聽不懂") != -1 or response_text == "":
        recordAudio()
        await sendrequest()
        print(response_text)
        response_text = ''

asyncio.run(main())