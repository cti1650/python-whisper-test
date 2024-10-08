import glob
import os
import whisper
import time
import difflib

def createTextFile(base_file_path, text, model_name=None):
  file_name = os.path.basename(base_file_path)
  if model_name:
    txt_file = '../output/' + file_name + f'_{model_name}.md'
  else:
    txt_file = '../output/' + file_name + '.md'
  print(f"input  : {base_file_path}")
  print(f"output : {txt_file}")
  with open(txt_file, 'w', encoding='utf-8') as f:
    f.write(text)

def highlight_diff(input_text, output_text):
  d = difflib.Differ()
  diff = list(d.compare(input_text, output_text))
  result = []
  correct_chars = 0
  i = 0
  while i < len(diff):
    if diff[i].startswith('  '):
      result.append(diff[i][2:])
      correct_chars += 1
      i += 1
    else:
      j = i
      deleted = []
      added = []
      while j < len(diff) and not diff[j].startswith('  '):
        if diff[j].startswith('- '):
          deleted.append(diff[j][2:])
        elif diff[j].startswith('+ '):
          added.append(diff[j][2:])
        j += 1
      
      if deleted and added:
        result.append(f'~~{"".join(deleted)}~~`{"".join(added)}`')
      elif deleted:
        result.append(f'~~{"".join(deleted)}~~')
      elif added:
        result.append(f'`{"".join(added)}`')
      
      i = j

  return ''.join(result), correct_chars

def calculate_recognition_rate(input_text, correct_chars):
  total_chars = len(input_text)
  recognition_rate = (correct_chars / total_chars) * 100
  return recognition_rate, correct_chars, total_chars

if __name__ == '__main__':
  model_list = [
    "tiny",
    "base",
    "small",
    "medium",
    # "large"
  ]
  model = dict.fromkeys(model_list)
  sample_input = {
    "data/sample1.mp3": "貴社の記者が汽車で帰社した。",
    "data/sample2.mp3": "この意見は革新的で核心を突いたものと私は確信している。",
    "data/sample3.mp3": "彼の遺志を医師から聞いて、それを継ぐ意志を固めた。",
    "data/sample4.mp3": "奇怪な機械を見る機会を得た。",
    "data/sample5.mp3": "イスタンブールは世界で唯一アジア大陸とヨーロッパ大陸にまたがる街で、この2つの大陸を分けているのがボスポラス海峡です。アジアとヨーロッパの間を進んでいく、壮大な体験ができる、ボスポラス海峡クルーズを堪能していただく予定です。"
  }

  print("start")
  for p in glob.iglob('data/sample*.mp*'):
    result_list = []
    for model_name in model_list:
      if not model_name:
        continue
      # 変換の実行
      print(f"model: {model_name}")
      if not model[model_name]:
        model[model_name] = whisper.load_model(model_name)
      start_time = time.perf_counter()
      result = model[model_name].transcribe(p, language="ja")
      result_text = result["text"]
      execution_time = round(time.perf_counter() - start_time, 4)
      
      # 差異をハイライトし、正しく認識された文字数を取得
      highlighted_text, correct_chars = highlight_diff(sample_input[p], result_text)
      
      # 認識率を計算
      recognition_rate, correct_chars, total_chars = calculate_recognition_rate(sample_input[p], correct_chars)
      
      if len(result_list) == 0:
        result_list.append(f"# Whisper音声認識検証\n\n## Input  \n{sample_input[p]}\n\n<audio controls src='../src/{p}'></audio>\n\n## Output")
      result_list.append(f"### {model_name} ( {str(execution_time)}s )\n{highlighted_text}\n\n認識率: {recognition_rate:.2f}% ({correct_chars}/{total_chars}文字)\n")
    
    createTextFile(p, "\n".join(result_list))

  print("完了")