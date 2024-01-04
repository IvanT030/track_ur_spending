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

current_datetime = datetime.now()
keys = ['sess-GxcoEBANtwvy0i1EhLOYGPb4GCyWJQIwlE7Jfq37','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', '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']
max_keys = 1
avliable_key = 0
y = current_datetime.year; m=current_datetime.month; d=current_datetime.day

speech_to_text = sr.Recognizer()
avliable_key = 0
response_text = ''

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
seconds = 7

p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

def recordAudio():
    global response_text
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
            #print("UnknownValueError")
            return
        print(text)
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
                print(response)
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

    return list1

async def main():
    global response_text
    while response_text.find("抱歉我聽不懂") != -1 or response_text == "":
        recordAudio()
        await sendrequest()
        print(response_text)
        for uncomplete_text in  check_text(response_text):
            match = re.compile(r'項目：([^，]+)，').search(uncomplete_text)
            print("檢測到項目：'"+match.group(1)+"'的錄音不完整，請重新錄製。")
    return response_text

asyncio.run(main())