import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
class SpeechToText:
  def __init__(self):
    self.rg = sr.Recognizer()

  def listen(self):
    with sr.Microphone() as source:
      self.rg.adjust_for_ambient_noise(source, duration=0.2)
      audioData = self.rg.listen(source)
      try:
        text = self.rg.recognize_google(audioData, language='zh-TW')
#         text = self.rg.recognize_whisper(audioData,model='base',language='chinese') # model tiny, base, small, medium, large, tiny.en, base.en, small.en, medium.en
      except:
        text = ''
    return text

  def __call__(self):
    return self.listen()

# convert text to speech
def text_to_speech(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

speech_to_text = SpeechToText()

text_to_speech('14個頭38隻腳，請問雞兔共幾隻？')
text = ''
while text == '':
    text = speech_to_text()
    if text=='':
      text_to_speech('聽不清楚')
    else:
      print(text)

text_to_speech(text)

if text.find('14')>=0:
    text_to_speech('答對了')
else:
    text_to_speech('答錯了')