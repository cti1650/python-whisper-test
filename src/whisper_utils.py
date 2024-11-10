import os
from datetime import timedelta
from typing import List, Dict, Optional
import shutil
from pathlib import Path
import whisper

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
        self.output_dir = output_dir
        self.input_dir = input_dir
        self.include_timestamps = include_timestamps
        self.timestamp_format = timestamp_format
        self.output_format = output_format
        self.language = language
        os.makedirs(output_dir, exist_ok=True)

    def set_model(self, model_name: str, device: str = 'cpu', compute_type: str = 'int8') -> None:
        """
        モデルの設定
        Args:
            model_name: モデル名 ('tiny', 'small', 'base', 'medium', 'large', 'large-v3')
            device: デバイス ('cpu' or 'cuda')
            compute_type: 計算精度 ('float16', 'int8_float16', 'int8')
        """
        self.model_name = model_name
        self.model = whisper.load_model(model_name)

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
        """Enhanced HTMLコンテンツの生成"""
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
        :root {{
            --header-height: 60px;
            --search-height: 60px;
            --player-height: 200px;
            --spacing: 20px;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            height: 100vh;
            overflow: hidden;
        }}
        
        .header {{
            height: var(--header-height);
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 0 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
        }}
        
        .main-container {{
            display: flex;
            height: calc(100vh - var(--header-height) - 40px);
            margin-top: var(--header-height);
            gap: var(--spacing);
            padding: var(--spacing);
        }}
        
        .media-container {{
            flex: 1;
            background: white;
            padding: var(--spacing);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            height: fit-content;
            position: sticky;
            top: calc(var(--header-height) + var(--spacing));
        }}
        
        .transcript-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: var(--spacing);
            max-width: 50%;
        }}
        
        .search-container {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .search-input {{
            width: 100%;
            box-sizing: border-box;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1em;
        }}
        
        .transcript-content {{
            background: white;
            padding: var(--spacing);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow-y: auto;
            height: calc(100vh - var(--header-height) - var(--search-height) - var(--spacing) * 4);
        }}
        
        {media_type} {{
            width: 100%;
            border-radius: 4px;
        }}
        
        .segment {{
            padding: 15px;
            margin: 5px 0;
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.2s;
            position: relative;
        }}
        
        .segment:hover {{
            background-color: #f0f0f0;
        }}
        
        .segment.active {{
            background-color: #e3f2fd;
        }}
        
        .segment.highlight {{
            background-color: #fff3cd;
        }}
        
        .timestamp {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
            user-select: none;
        }}
        
        .text {{
            line-height: 1.5;
        }}
        
        .text[contenteditable="true"] {{
            border: 1px solid #ddd;
            padding: 5px;
            border-radius: 4px;
        }}
        
        .segment-actions {{
            display: none;
            position: absolute;
            right: 10px;
            top: 10px;
            gap: 5px;
        }}
        
        .segment:hover .segment-actions {{
            display: flex;
        }}
        
        .btn {{
            padding: 5px 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9em;
            background: #f0f0f0;
            transition: background-color 0.2s;
        }}
        
        .btn:hover {{
            background: #e0e0e0;
        }}
        
        .header-actions {{
            display: flex;
            gap: 10px;
        }}
        
        .tooltip {{
            position: fixed;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.9em;
            pointer-events: none;
            z-index: 1000;
        }}
        
        @media (max-width: 768px) {{
            .main-container {{
                flex-direction: column;
            }}
            
            .media-container, .transcript-container {{
                max-width: 100%;
            }}
            
            .media-container {{
                position: static;
            }}
            
            .transcript-content {{
                height: auto;
                max-height: 50vh;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>文字起こし - {media_filename}</h1>
        <div class="header-actions">
            <button class="btn" id="copy-all">全体をコピー</button>
            <button class="btn" id="copy-all-with-timestamps">タイムスタンプ付きでコピー</button>
        </div>
    </div>
    
    <div class="main-container">
        <div class="media-container">
            <{media_type} id="media-player" controls>
                <source src="{media_filename}" type="{media_type}/{media_ext[1:]}">
                お使いのブラウザは{media_type}タグをサポートしていません。
            </{media_type}>
        </div>
        
        <div class="transcript-container">
            <div class="search-container">
                <input type="text" class="search-input" placeholder="テキストを検索..." id="search-input">
            </div>
            
            <div class="transcript-content" id="transcript">
                {self._generate_segments_html(segments)}
            </div>
        </div>
    </div>
    
    <script>
        const player = document.getElementById('media-player');
        const transcript = document.getElementById('transcript');
        const segments = document.querySelectorAll('.segment');
        const searchInput = document.getElementById('search-input');
        let currentSegment = null;
        let tooltip = null;
        
        // ツールチップ作成
        function createTooltip() {{
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.style.display = 'none';
            document.body.appendChild(tooltip);
            return tooltip;
        }}
        
        // テキストコピー機能
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(() => {{
                showTooltip('コピーしました');
            }});
        }}
        
        // ツールチップ表示
        function showTooltip(text, x = null, y = null) {{
            if (!tooltip) {{
                tooltip = createTooltip();
            }}
            
            tooltip.textContent = text;
            tooltip.style.display = 'block';
            
            if (x !== null && y !== null) {{
                tooltip.style.left = `${{x}}px`;
                tooltip.style.top = `${{y}}px`;
            }} else {{
                // デフォルト位置（画面中央上部）
                tooltip.style.left = '50%';
                tooltip.style.top = '10%';
                tooltip.style.transform = 'translateX(-50%)';
            }}
            
            setTimeout(() => {{
                tooltip.style.display = 'none';
            }}, 2000);
        }}
        
        // 検索機能
        searchInput.addEventListener('input', () => {{
            const searchText = searchInput.value.toLowerCase();
            segments.forEach(segment => {{
                const text = segment.querySelector('.text').textContent.toLowerCase();
                segment.classList.toggle('highlight', searchText ? text.includes(searchText) : false);
            }});
        }});
        
        // セグメントの編集機能
        segments.forEach(segment => {{
            const textDiv = segment.querySelector('.text');
            const timestamp = segment.querySelector('.timestamp').textContent;

            // 再生ボタン
            const playBtn = document.createElement('button');
            playBtn.className = 'btn';
            playBtn.textContent = '再生';
            playBtn.onclick = (e) => {{
                e.stopPropagation();
                const start = parseFloat(segment.dataset.start);
                player.currentTime = start;
                player.play();
            }};
            
            // 編集ボタン
            const editBtn = document.createElement('button');
            editBtn.className = 'btn';
            editBtn.textContent = '編集';
            editBtn.onclick = (e) => {{
                e.stopPropagation();
                textDiv.contentEditable = textDiv.contentEditable === 'true' ? 'false' : 'true';
                editBtn.textContent = textDiv.contentEditable === 'true' ? '保存' : '編集';
                if (textDiv.contentEditable === 'true') {{
                    player.pause();
                    textDiv.focus();
                }}
            }};
            
            // コピーボタン
            const copyBtn = document.createElement('button');
            copyBtn.className = 'btn';
            copyBtn.textContent = 'コピー';
            copyBtn.onclick = (e) => {{
                e.stopPropagation();
                const textToCopy = textDiv.textContent.trim();
                copyToClipboard(textToCopy);
            }};
            
            // タイムスタンプ付きコピーボタン
            const copyWithTimestampBtn = document.createElement('button');
            copyWithTimestampBtn.className = 'btn';
            copyWithTimestampBtn.textContent = 'TS付きコピー';
            copyWithTimestampBtn.onclick = (e) => {{
                e.stopPropagation();
                const textToCopy = `${{timestamp}} ${{textDiv.textContent.trim()}}`;
                copyToClipboard(textToCopy);
            }};
            
            // ボタンコンテナ
            const actions = document.createElement('div');
            actions.className = 'segment-actions';
            actions.append(playBtn, editBtn, copyBtn, copyWithTimestampBtn);
            segment.appendChild(actions);
        }});
        
        // 全体コピー機能
        document.getElementById('copy-all').onclick = () => {{
            const allText = Array.from(segments)
                .map(segment => segment.querySelector('.text').textContent.trim())
                .join('\\n');
            copyToClipboard(allText);
        }};
        
        document.getElementById('copy-all-with-timestamps').onclick = () => {{
            const allText = Array.from(segments)
                .map(segment => {{
                    const timestamp = segment.querySelector('.timestamp').textContent;
                    const text = segment.querySelector('.text').textContent.trim();
                    return `${{timestamp}} ${{text}}`;
                }})
                .join('\\n');
            copyToClipboard(allText);
        }};
        
        // セグメントクリック時の再生
        // segments.forEach(segment => {{
        //     segment.addEventListener('click', () => {{
        //         const start = parseFloat(segment.dataset.start);
        //         player.currentTime = start;
        //         player.play();
        //     }});
        // }});
        
        // 再生位置に応じたセグメントのハイライトと自動スクロール
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
                        transcript.scrollTop = segment.offsetTop - transcript.offsetTop;
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
        segments: List[Dict]
    ) -> None:
        """出力ファイルの作成"""
        file_name = os.path.basename(base_file_path)
        base_name = os.path.splitext(file_name)[0]

        if not self.model_name:
            return
        
        if self.model_name:
            output_name = f"{base_name}_{self.model_name}"
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
        file_path: str
    ) -> bool:
        """音声ファイルの処理"""
        print(f"Processing: {file_path}")
        try:
            if not self.model or not self.model_name:
                print("Model not set. Please set the model before processing.")
                return False
            result = self.model.transcribe(
                file_path,
                language=self.language,
                word_timestamps=True,  # HTML出力の場合は常にTrue
                verbose=True,
            )
            self.create_output_file(file_path, result["segments"])
            return True
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return False