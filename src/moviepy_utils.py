import os
from moviepy.editor import VideoFileClip, AudioFileClip

def convert_audio_file(audio_path):
    current_path = os.path.abspath(audio_path)
    file_extension = os.path.splitext(current_path)[-1].lower()

    # .movファイルを.mp4に変換
    if file_extension == '.mov':
        mp4_path = current_path.replace('.mov', '.mp4')
        with VideoFileClip(current_path) as clip:
            clip.write_videofile(mp4_path, codec="libx264")
        current_path = mp4_path
        os.remove(audio_path)

    # .m4aファイルを.mp3に変換
    elif file_extension == '.m4a':
        mp3_path = current_path.replace('.m4a', '.mp3')
        with AudioFileClip(current_path) as clip:
            clip.write_audiofile(mp3_path)
        current_path = mp3_path
        os.remove(audio_path)
    return current_path