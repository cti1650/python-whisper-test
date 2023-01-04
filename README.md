# Python Whisper Test

## Docker操作

- Dockerビルド
  ```
  docker-compose build
  ```

- Docker起動
  ```
  docker-compose up -d
  ```

- Docker起動状況確認
  ```
  docker-compose ps
  ```

- Docker停止
  ```
  docker-compose stop
  ```

- Docker終了
  ```
  docker-compose down
  ```

## コマンドで実行

- Whisper起動
  ```
  docker-compose exec whisper /bin/bash
  ```

- Whisperで文字起こし
  ```
  whisper <音声ファイルの名前.拡張子> --language ja
  ```

- Whisper停止
  ```
  exit
  ```

## Pythonで実行

  - `src/audio.mp3`ファイルの書き出し結果を表示する。
    ```
    docker-compose exec -it python3 python sample.py
    ```


  - inputディレクトリに音声データを格納して以下のコマンドを実行すると認識結果をoutputディレクトリに書き出しする。
    ```
    docker-compose exec -it python3 python main.py
    ```

## Whisper モデル一覧

![モデル一覧](https://raw.githubusercontent.com/cm-nakamura-shogo/devio-image/main/whisper-trial-japanese/img/whisper-trial-japanese_2022-09-22-21-53-13.png)

## 参考サイト

- [OpenAIリリースのWhisperで文字起こし後にテキスト読み上げした話](https://dev.classmethod.jp/articles/transform-whisper-txt-into-audio-file/)  
- [OpenAI Whisper のコマンドオプション - Qiita](https://qiita.com/szktmyk38f/items/374f24d06fe277a1922a)  
- [WhisperのREADME](https://zenn.dev/piment/articles/ca917d0e9c8a49)  
- [DockerとDocker ComposeでPythonの実行環境を作成する | ZUMA Lab](https://zuma-lab.com/posts/docker-python-settings)  
- [OpenAIがリリースした高精度な音声認識モデル”Whisper”を使って、オンライン会議の音声を書き起こししてみた | DevelopersIO](https://dev.classmethod.jp/articles/whisper-trial-japanese/)  
