import speech_recognition as sr
from transformers import pipeline
from googletrans import Translator

# Step 1: Convert Audio to Text
recognizer = sr.Recognizer()

with sr.AudioFile("lecture.wav") as source:
    audio = recognizer.record(source)

print("Converting speech to text...")

text = recognizer.recognize_google(audio)

print("\nFull Lecture Text:")
print(text)

# Step 2: Summarize Text using AI
print("\nGenerating Notes...")

summarizer = pipeline("summarization")

summary = summarizer(text, max_length=100, min_length=30, do_sample=False)

notes = summary[0]['summary_text']

print("\nAI Generated Notes:")
print(notes)

# Step 3: Translate Notes
translator = Translator()

translated = translator.translate(notes, dest='hi')

print("\nTranslated Notes (Hindi):")
print(translated.text)