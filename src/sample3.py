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
  in_diff = False
  for line in diff:
    if line.startswith('  '):
      if in_diff:
        result.append('`')
        in_diff = False
      result.append(line[2:])
    elif line.startswith('- '):
      continue
    elif line.startswith('+ '):
      if not in_diff:
        result.append('`')
        in_diff = True
      result.append(line[2:])
  if in_diff:
    result.append('`')
  return ''.join(result)

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
      
      # 差異をハイライト
      highlighted_text = highlight_diff(sample_input[p], result_text)
      
      if len(result_list) == 0:
        result_list.append(f"# Whisper音声認識検証\n\n## Input  \n{sample_input[p]}\n\n<audio controls src='../src/{p}'></audio>\n\n## Output")
      result_list.append(f"### {model_name} ( {str(execution_time)}s )\n{highlighted_text}\n")
    
    createTextFile(p, "\n".join(result_list))

  print("完了")