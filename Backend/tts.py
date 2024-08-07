from gtts import gTTS
import os
import ffmpeg
import subprocess


def text_to_speech(text):
    # Initialize gTTS with the text to convert
    speech = gTTS(text, lang="en", tld="us")

    # Save the audio file to a temporary file
    speech_file = "./Backend/speech.mp3"
    speech.save(speech_file)

    # Temporary file for the pitch adjusted output
    temp_file = "./Backend/speech_temp.mp3"

    # Pitch adjustment
    (
        ffmpeg.input(speech_file)
        .filter("asetrate", 24000 * 1.05)
        .filter("aresample", 24000)
        .filter("atempo", 1.3)
        .output(temp_file)
        .run(overwrite_output=True)
    )
    os.replace(temp_file, speech_file)
    subprocess.run(["ffplay", "-autoexit", "-nodisp", speech_file])
