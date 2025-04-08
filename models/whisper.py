import whisper


model = whisper.load_model("base")

def transcribe(audio):
    return model.transcribe(audio)
