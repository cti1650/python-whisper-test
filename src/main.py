import glob
import os
import whisper

def createTextFile(base_file_path, text, model_name=None):
  file_name = os.path.basename(base_file_path)
  if model_name:
    txt_file = '../output/' + file_name + f'_{model_name}.txt'
  else:
    txt_file = '../output/' + file_name + '.txt'
  print(f"input  : {base_file_path}")
  print(f"output : {txt_file}")
  f = open(txt_file, 'w')
  f.write(text)
  f.close()

if __name__ == '__main__':  # インポート時には動かない

  model_list = [
    # "tiny",
    # "base",
    "small",
    # "medium",
    # "large"
  ]

  print("start")
  for model_name in model_list:
    if not model_name:
      continue
    # 変換の実行
    print(f"model: {model_name}")
    model = whisper.load_model(model_name)
    for p in glob.iglob('../input/*'):
      result = model.transcribe(p)
      result_text = result["text"]
      createTextFile(p, result_text, model_name)
      