import os
import glob
import whisper
from whisper_utils import WhisperProcessor
from moviepy.editor import VideoFileClip, AudioFileClip
from config import WHISPER_CONFIG

def main():
    processor = WhisperProcessor(
        output_dir=WHISPER_CONFIG['paths']['output'],
        input_dir=WHISPER_CONFIG['paths']['input'],
        include_timestamps=WHISPER_CONFIG['timestamps']['include'],
        timestamp_format=WHISPER_CONFIG['timestamps']['format'],
        output_format=WHISPER_CONFIG['output_format']
    )
    
    print("Starting transcription process...")
    print(f"Output format: {processor.output_format}")
    
    for model_name in WHISPER_CONFIG['models']['available']:
        print(f"Loading model: {model_name}")
        model = whisper.load_model(model_name)
        
        for audio_path in glob.iglob(os.path.join(processor.input_dir, '*')):
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
            processor.process_audio_file(current_path, model, model_name)

    print("Transcription complete!")

if __name__ == '__main__':
    main()