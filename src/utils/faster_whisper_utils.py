from utils.whisper_utils import WhisperProcessor
from faster_whisper import WhisperModel

class FasterWhisperProcessor(WhisperProcessor):
    def __init__(
        self, 
        output_dir: str = '../output',
        input_dir: str = '../input',
        include_timestamps: bool = True,
        timestamp_format: str = 'full',
        output_format: str = 'txt',  # 'txt' or 'html'
        language: str = 'ja' # 'ja' or 'en'
    ):
        """
        WhisperProcessor初期化
        Args:
            output_dir: 出力ディレクトリのパス
            input_dir: 入力ディレクトリのパス
            include_timestamps: タイムスタンプを含めるかどうか
            timestamp_format: タイムスタンプのフォーマット ('full' or 'simple')
            output_format: 出力フォーマット ('txt' or 'html')
        """
        super().__init__(output_dir, input_dir, include_timestamps, timestamp_format, output_format, language)

    def set_model(self, model_name: str, device: str = 'cpu', compute_type: str = 'int8') -> None:
        """
        モデルの設定
        Args:
            model_name: モデル名 ('tiny', 'small', 'base', 'medium', 'large', 'large-v3')
            device: デバイス ('cpu' or 'cuda')
            compute_type: 計算精度 ('float16', 'int8_float16', 'int8')
        """
        self.model_name = model_name
        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def process_audio_file(
        self,
        file_path: str
    ) -> bool:
        """音声ファイルの処理"""
        print(f"Processing: {file_path}")
        try:
            if not self.model or not self.model_name:
                print("Model not set. Please set the model before processing.")
                return False
            segments, info = self.model.transcribe(
                file_path,
                language=self.language,
                word_timestamps=True,  # HTML出力の場合は常にTrue
                beam_size=5,
                vad_filter=True,
            )
            self.create_output_file(file_path, 
                list({
                    'text': segment.text,
                    'start': segment.start,
                    'end': segment.end
                } for segment in segments))
            return True
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return False