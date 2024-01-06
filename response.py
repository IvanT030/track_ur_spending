# -*- coding: utf-8 -*-
import pyaudio
import re
import wave
import speech_recognition as sr
import openai
from openai import AsyncOpenAI
import sys
sys.stdout.encoding
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
from datetime import datetime
import asyncio
import sqlite3
import tkinter as tk
import threading

current_datetime = datetime.now()
keys = ['sess-GxcoEBANtwvy0i1EhLOYGPb4GCyWJQIwlE7Jfq37','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', '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']
max_keys = 1
avliable_key = 0
y = current_datetime.year; m=current_datetime.month; d=current_datetime.day

speech_to_text = sr.Recognizer()
avliable_key = 0
response_text = ''

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

async def sendrequest():
    global avliable_key
    global response_text
    with sr.AudioFile("output.wav") as source:
        audio = speech_to_text.record(source)
        try:
            text = speech_to_text.recognize_google(audio, language='zh-TW')
        except sr.exceptions.UnknownValueError as e:
            result_text.set("I can't hear you, please click the microphone to start recording again.")
            return
        result_text.set("Processing...... this may take a few seconds")
        while response_text == "":
            #print("using " + str(avliable_key) + " key")
            client = AsyncOpenAI(api_key=keys[avliable_key],)
            try:
                response = await client.chat.completions.create(
                    model='gpt-3.5-turbo',
                    messages= [
                        {"role": "system", "content": "你是個記帳輔助員，你要幫要照我的規則來幫我記帳"},
                        {"role": "user", "content": "我上個月在吃了300元的牛肉麵，今天是2024年1月3日，品項在以下分類：餐飲、生活、娛樂、交通、投資、醫療、其他"},
                        {"role": "assistant", "content": "項目：牛肉麵，餐飲，2023年12月3日，300。"},
                        {"role": "user", "content": "我前天超商花105元，今天是2012年6月8日，品項在以下分類：餐飲、生活、娛樂、交通、投資、醫療、其他"},
                        {"role": "assistant", "content": "項目：超商，生活，2012年6月6日，105。"},
                        {"role": "user", "content": "我說說超108元，今天是2000年8月9日，品項在以下分類：餐飲、生活、娛樂、交通、投資、醫療、其他"},
                        {"role": "assistant", "content": "抱歉我聽不懂"},
                        {"role": "user", "content": "我3月8日跟朋友喝酒花了500元，今天是2023年5月6日，品項在以下分類：餐飲、生活、娛樂、交通、投資、醫療、其他"},
                        {"role": "assistant", "content": "項目：喝酒，餐飲，2023年3月8日，500。"},
                        {"role": "user", "content": "114元商店我2023年78月，今天是2000年8月9日，品項在以下分類：餐飲、生活、娛樂、交通、投資、醫療、其他"},
                        {"role": "assistant", "content": "抱歉我聽不懂"},
                        {"role": "user", "content": "我剛剛花500吃飯順便去打保齡球花了150，今天是2023年5月6日，品項在以下分類：餐飲、生活、娛樂、交通、投資、醫療、其他"},
                        {"role": "assistant", "content": "項目：吃飯，餐飲，2023年5月6日，500。項目：保齡球，娛樂，2023年5月6日，150。"},
                        {"role": "user", "content": "cksjdsdqoiwodkfkd，現在我有冰淇淋，今天是1989年6月4日，品項在以下分類：餐飲、生活、娛樂、交通、投資、醫療、其他"},
                        {"role": "assistant", "content": "抱歉我聽不懂"},
                        {"role": "user", "content": "我上個月去壽司郎花800，去年投了美股賠了1萬3，今天搭車花了70，今天是2011年3月22日，品項在以下分類：餐飲、生活、娛樂、交通、投資、醫療、其他"},
                        {"role": "assistant", "content": "項目：壽司郎，餐飲，2011年2月22日，800。項目：投美股，投資，2010年3月22日，13000。項目：搭車，交通，2011年3月22日，70。"},
                        {"role": "user", "content": "昨天住院花了2萬，前天賭博書了6千，大前天去應酬掏了2千元，我好慘喔，今天是2020年7月7日，品項在以下分類：餐飲、生活、娛樂、交通、投資、醫療、其他"},
                        {"role": "assistant", "content": "項目：住院，醫療，2020年7月6日，20000。項目：賭博，其他，2020年7月6日，6000。項目：應酬，其他，2020年7月5日，2000。"},
                        {"role": "user", "content": "，去年11月去漫展花了兩千二，兩個禮拜前又去一次花了七千，今天是2011年10月30日，品項在以下分類：餐飲、生活、娛樂、交通、投資、醫療、其他"},
                        {"role": "assistant", "content": "項目：漫展，娛樂，2010年11月30日，2200。項目：漫展，娛樂，2011年10月16日，7000。"},
                        {"role": "user", "content": text + f"今天是{y}年{m}月{d}日，品項在以下分類：餐飲、生活、娛樂、交通、投資、醫療、其他"}
                    ],
                    temperature=0.3
                )
                #print(response)
                response_text = response.choices[0].message.content
            except openai.RateLimitError as e:
                if avliable_key == max_keys:
                    avliable_key = 0
                else :
                    avliable_key += 1
                #print("RateLimitError")

def check_text(text):
    paragraphs = text.split('。')
    # 定義正規表達式模式
    pattern = re.compile(r'(?:項目：)?([^，]+)，([^，]+)，(\d{4})年(\d+)月(\d+)日，(\d+)')
    # 定義存放結果的列表
    list1 = []  # 有缺少的段落
    list2 = []  # 沒有缺少的段落
    # 使用正規表達式檢查每段
    for paragraph in paragraphs:
        if paragraph:  # 確保不處理空的段落
            match = pattern.match(paragraph)
            if match and len(match.groups()) == 6:
                list2.append(match.groups())
            elif "項目：" in paragraph:
                list1.append(paragraph)
    return list1, list2

async def main():
    global response_text
    while response_text.find("抱歉我聽不懂") != -1 or response_text == "":
        err = ""
        err = await sendrequest()
        if err == "ValueError":
            print("未接收到聲音，請重新錄製。")
            continue
        print(response_text)
        uncomplete_text, complete_text = check_text(response_text)
        for ut in uncomplete_text:
            match = re.compile(r'項目：([^，]+)，').search(ut)
            print("檢測到項目：'"+match.group(1)+"'的錄音不完整，請重新錄製。")
    return complete_text

conn = sqlite3.connect('track_your_spending.db')
c = conn.cursor()
#or text in result:
#    c.execute(f"""INSERT INTO spending 
#        (Year,Month,Day,Spending_Category,Expense_Item,Cost)
#        VALUES ({text[2]}, {text[3]}, {text[4]}, '{text[1]}', '{text[0]}', {text[5]})""")

# Function to handle clicking on the microphone button.
uncomplete_text = []; complete_text = []

async def async_toggle_recording():
    if not recorder.is_recording:
        recorder.start_recording()
        microphone_button.config(text='🔴 Recording...')
    else:
        global complete_text, uncomplete_text
        recorder.stop_recording()
        microphone_button.config(text='')
        await sendrequest()
        uncomplete_text, complete_text = check_text(response_text)
        if response_text == "" or  response_text.find("抱歉我聽不懂") >= 1:
            result_text.set("Sorry, I don't understand. Please record it again. :( ")
            microphone_button.config(text='🎤 Start Recording')
        else:
            result_text.set("Done! Press OK to save data or Cancel to re-record.") #要改uncompletetext + complete_text
loop = asyncio.new_event_loop()
def start_async_toggle_recording():
    # 在異步事件循環中運行 async_toggle_recording
    asyncio.run_coroutine_threadsafe(async_toggle_recording(), loop)
def run_asyncio_loop():
    loop.run_forever()
threading.Thread(target=run_asyncio_loop, daemon=True).start()

# Function to handle the OK button click.
def on_ok_click():
    global complete_text
    if complete_text.len > 0:
        result_text.set("Data Saved! Please click the microphone to start recording.")
        microphone_button.config(text='🎤 Start Recording')
        complete_text =  [], uncomplete_text = []

# Function to handle the Cancel button click.
def on_cancel_click():
    global complete_text
    if complete_text.len > 0:
        result_text.set("Data Saved! Please click the microphone to start recording.")
        microphone_button.config(text='🎤 Start Recording')
        complete_text =  [], uncomplete_text = []

root = tk.Tk()
root.title("Voice-Controlled Accounting System")

# Result text variable
microphone_button = tk.Button(root, text="🎤 Start Recording", command=start_async_toggle_recording)
microphone_button.pack()

# Microphone text
result_text = tk.StringVar()
result_text.set("Please click the microphone to start recording.")

# Result display
result_label = tk.Label(root, textvariable=result_text)
result_label.pack()

# OK button
ok_button = tk.Button(root, text="OK", command=on_ok_click)
ok_button.pack(side=tk.LEFT)

# Cancel button
cancel_button = tk.Button(root, text="Cancel", command=on_cancel_click)
cancel_button.pack(side=tk.RIGHT)

# Run the application
recorder = AudioRecorder()
root.mainloop()
conn.commit()
conn.close()