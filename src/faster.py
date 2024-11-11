import os
import glob
from utils.faster_whisper_utils import FasterWhisperProcessor
from utils.moviepy_utils import convert_audio_file
from config import WHISPER_CONFIG

def faster(language = None):
    processor = FasterWhisperProcessor(
        output_dir=WHISPER_CONFIG['paths']['output'],
        input_dir=WHISPER_CONFIG['paths']['input'],
        include_timestamps=WHISPER_CONFIG['timestamps']['include'],
        timestamp_format=WHISPER_CONFIG['timestamps']['format'],
        output_format=WHISPER_CONFIG['output_format'],
        language=WHISPER_CONFIG['language'] if language is None else language
    )
    
    print("Starting transcription process...")
    print(f"Output format: {processor.output_format}")
    
    for model_name in WHISPER_CONFIG['models']['available']:
        print(f"Loading model: {model_name}")
        processor.set_model(model_name, device=WHISPER_CONFIG['device'], compute_type=WHISPER_CONFIG['compute_type'])
        
        for audio_path in glob.iglob(os.path.join(processor.input_dir, '*')):
            current_path = convert_audio_file(audio_path)
            processor.process_audio_file(current_path)

    print("Transcription complete!")

if __name__ == '__main__':
    faster()