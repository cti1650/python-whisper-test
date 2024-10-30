import os
import glob
import whisper
from whisper_utils import WhisperProcessor
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
            processor.process_audio_file(audio_path, model, model_name)

    print("Transcription complete!")

if __name__ == '__main__':
    main()