import whisper

model = whisper.load_model("small")
result = model.transcribe("data/audio.mp3")
print(result["text"])