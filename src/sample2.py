import glob
import os
import whisper
import time

def createTextFile(base_file_path, text, model_name=None):
  file_name = os.path.basename(base_file_path)
  if model_name:
    txt_file = '../output/' + file_name + f'_{model_name}.md'
  else:
    txt_file = '../output/' + file_name + '.md'
  print(f"input  : {base_file_path}")
  print(f"output : {txt_file}")
  f = open(txt_file, 'w')
  f.write(text)
  f.close()

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
    "data/sample4.mp3": "奇怪な機械を見る機会を得た。"
  }

  print("start")
  for p in glob.iglob('data/sample*.mp3'):
    result_list = []
    for model_name in model_list:
      if not model_name:
        continue
      # 変換の実行
      print(f"model: {model_name}")
      if not model[model_name]:
        model[model_name] = whisper.load_model(model_name)
      start_time = time.perf_counter()
      result = model[model_name].transcribe(p)
      result_text = result["text"]
      execution_time = round(time.perf_counter() - start_time,4)
      if len(result_list) == 0:
        result_list.append(f"# Whisper音声認識検証\n\n## Input  \n{sample_input[p]}\n\n<audio controls src='../src/{p}'></audio>\n\n## Output")
      result_list.append(f"### {model_name} ( {str(execution_time)}s )\n{result_text}\n")
    
    createTextFile(p, "\n".join(result_list))