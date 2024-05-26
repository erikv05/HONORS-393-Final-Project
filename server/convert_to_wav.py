from pydub import AudioSegment
import re

def convert_to_wav(filepath):
    pattern = r'[^\/]+(?=\.)'
    if len(filepath) < 4:
        raise Exception("Invalid filepath.")
    
    if filepath[-4:] == ".mp3":
        sound = AudioSegment.from_file(filepath, format="mp3")
        sound.export(f"converted_wavfiles/{re.findall(pattern, filepath)[0]}.wav", format="wav")
    elif filepath[-4:] == ".m4a":
        sound = AudioSegment.from_file(filepath, format="m4a")
        sound.export(f"converted_wavfiles/{re.findall(pattern, filepath)[0]}.wav")
    else:
        raise Exception("Not a valid m4a or mp3 file.")