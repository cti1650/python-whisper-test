import os
from datetime import timedelta
from typing import List, Dict, Optional
import shutil
from pathlib import Path

def format_timestamp(seconds: float) -> str:
    """秒数を[HH:MM:SS.mmm]形式に変換"""
    td = timedelta(seconds=seconds)
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = td.seconds % 60
    milliseconds = int(td.microseconds / 1000)
    return f"[{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}]"

class WhisperProcessor:
    def __init__(
        self, 
        output_dir: str = '../output',
        input_dir: str = '../input',
        include_timestamps: bool = True,
        timestamp_format: str = 'full',
        output_format: str = 'txt'  # 'txt' or 'html'
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
        self.output_dir = output_dir
        self.input_dir = input_dir
        self.include_timestamps = include_timestamps
        self.timestamp_format = timestamp_format
        self.output_format = output_format
        os.makedirs(output_dir, exist_ok=True)

    def format_line(self, segment: Dict) -> str:
        """セグメントを指定されたフォーマットで文字列に変換"""
        text = segment['text'].strip()
        
        if not self.include_timestamps:
            return f"{text}\n"
            
        start_time = format_timestamp(segment['start'])
        end_time = format_timestamp(segment['end'])
        
        if self.timestamp_format == 'simple':
            simple_start = f"[{int(segment['start'])//60:02d}:{int(segment['start'])%60:02d}]"
            return f"{simple_start} {text}\n"
        else:
            return f"{start_time} -> {end_time}: {text}\n"

    def generate_html_content(self, segments: List[Dict], media_file: str) -> str:
        """HTMLコンテンツの生成"""
        media_filename = os.path.basename(media_file)
        media_ext = os.path.splitext(media_filename)[1].lower()
        is_video = media_ext in ['.mp4', '.webm', '.ogg']
        media_type = 'video' if is_video else 'audio'
        
        html_template = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文字起こし - {media_filename}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }}
        .media-container {{
            flex: 1;
            position: sticky;
            top: 20px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .transcript-container {{
            flex: 1;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .segment {{
            padding: 10px;
            margin: 5px 0;
            cursor: pointer;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}
        .segment:hover {{
            background-color: #f0f0f0;
        }}
        .segment.active {{
            background-color: #e3f2fd;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
        }}
        {media_type} {{
            width: 100%;
            border-radius: 4px;
        }}
        @media (max-width: 768px) {{
            .container {{
                flex-direction: column;
            }}
            .media-container {{
                position: static;
            }}
        }}
    </style>
</head>
<body>
    <h1>文字起こし - {media_filename}</h1>
    <div class="container">
        <div class="media-container">
            <{media_type} id="media-player" controls>
                <source src="{media_filename}" type="{media_type}/{media_ext[1:]}">
                お使いのブラウザは{media_type}タグをサポートしていません。
            </{media_type}>
        </div>
        <div class="transcript-container">
            <div id="transcript">
                {self._generate_segments_html(segments)}
            </div>
        </div>
    </div>
    <script>
        const player = document.getElementById('media-player');
        const segments = document.querySelectorAll('.segment');
        let currentSegment = null;

        // セグメントクリック時の処理
        segments.forEach(segment => {{
            segment.addEventListener('click', () => {{
                const start = parseFloat(segment.dataset.start);
                player.currentTime = start;
                player.play();
            }});
        }});

        // 再生位置に応じてセグメントをハイライト
        player.addEventListener('timeupdate', () => {{
            const currentTime = player.currentTime;
            segments.forEach(segment => {{
                const start = parseFloat(segment.dataset.start);
                const end = parseFloat(segment.dataset.end);
                
                if (currentTime >= start && currentTime <= end) {{
                    if (currentSegment !== segment) {{
                        if (currentSegment) {{
                            currentSegment.classList.remove('active');
                        }}
                        segment.classList.add('active');
                        currentSegment = segment;
                        
                        // スクロール位置の調整
                        const container = document.getElementById('transcript');
                        const segmentTop = segment.offsetTop;
                        const containerTop = container.scrollTop;
                        const containerHeight = container.clientHeight;
                        
                        if (segmentTop < containerTop || segmentTop > containerTop + containerHeight) {{
                            segment.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                        }}
                    }}
                }}
            }});
        }});
    </script>
</body>
</html>
        """
        return html_template

    def _generate_segments_html(self, segments: List[Dict]) -> str:
        """セグメントのHTML生成"""
        segments_html = ""
        for segment in segments:
            start = segment['start']
            end = segment['end']
            text = segment['text'].strip()
            timestamp = f"{int(start//60):02d}:{int(start%60):02d} - {int(end//60):02d}:{int(end%60):02d}"
            
            segments_html += f"""
                <div class="segment" data-start="{start}" data-end="{end}">
                    <div class="timestamp">{timestamp}</div>
                    <div class="text">{text}</div>
                </div>
            """
        return segments_html

    def create_output_file(
        self,
        base_file_path: str,
        segments: List[Dict],
        model_name: Optional[str] = None
    ) -> None:
        """出力ファイルの作成"""
        file_name = os.path.basename(base_file_path)
        base_name = os.path.splitext(file_name)[0]
        
        if model_name:
            output_name = f"{base_name}_{model_name}"
        else:
            output_name = base_name

        if self.output_format == 'html':
            # HTMLファイル作成
            html_file = os.path.join(self.output_dir, f"{output_name}.html")
            html_content = self.generate_html_content(segments, file_name)
            
            # 元のメディアファイルを出力ディレクトリにコピー
            media_dest = os.path.join(self.output_dir, file_name)
            shutil.copy2(base_file_path, media_dest)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"input  : {base_file_path}")
            print(f"output : {html_file}")
            print(f"media  : {media_dest}")
        else:
            # テキストファイル作成
            txt_file = os.path.join(self.output_dir, f"{output_name}.txt")
            with open(txt_file, 'w', encoding='utf-8') as f:
                for segment in segments:
                    f.write(self.format_line(segment))
            
            print(f"input  : {base_file_path}")
            print(f"output : {txt_file}")

    def process_audio_file(
        self,
        file_path: str,
        model,
        model_name: Optional[str] = None
    ) -> bool:
        """音声ファイルの処理"""
        print(f"Processing: {file_path}")
        try:
            result = model.transcribe(
                file_path,
                language="ja",
                verbose=True,
                word_timestamps=True  # HTML出力の場合は常にTrue
            )
            self.create_output_file(file_path, result["segments"], model_name)
            return True
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return False