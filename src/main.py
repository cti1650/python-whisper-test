import glob
import os
import whisper

if __name__ == '__main__':  # インポート時には動かない

  model_name = "small"

  # 変換の実行
  print("start")
  model = whisper.load_model(model_name)
  for p in glob.iglob('../input/*'):
    print(f"input  : {p}")
    result = model.transcribe(p)
    result_text = result["text"]
    file_name = os.path.basename(p)
    txt_file = '../output/' + file_name + f'_{model_name}.txt'
    print(f"output : {txt_file}")
    f = open(txt_file, 'w')
    f.write(result_text)
    f.close()