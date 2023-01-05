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

  - サンプル音声の書き出し結果をコマンド上で表示する。
    ```
    docker-compose exec -it python3 python sample.py

    or

    # Dockerの起動と停止も合わせて実施
    sh run_sample.sh
    ```

    - src/data/audio.mp3
      > イスタンブールは世界で唯一アジア大陸とヨーロッパ大陸にまたがる街で、この2つの大陸を分けているのがボスポラス海峡です。アジアとヨーロッパの間を進んでいく、壮大な体験ができる、ボスポラス海峡クルーズを単納していただく予定です。

  - サンプル音声を変換
    ```
    docker-compose exec -it python3 python sample2.py

    or

    # Dockerの起動と停止も合わせて実施
    sh run_sample2.sh
    ```

    - data/sample1.mp3  
      > 貴社の記者が汽車で帰社した。

    - data/sample2.mp3
      > この意見は革新的で核心を突いたものと私は確信している。

    - data/sample3.mp3
      > 彼の遺志を医師から聞いて、それを継ぐ意志を固めた。

    - data/sample4.mp3
      > 奇怪な機械を見る機会を得た。


    ※ 読み上げ（テキスト→音声変換）で変換(女性C)  
    https://choimitena.com/Text/Convert


  - inputディレクトリに音声データを格納して以下のコマンドを実行すると認識結果をoutputディレクトリに書き出しする。
    ```
    docker-compose exec -it python3 python main.py

    or

    # Dockerの起動と停止も合わせて実施
    sh run_main.sh
    ```

## Whisper モデル一覧

![モデル一覧](https://raw.githubusercontent.com/cm-nakamura-shogo/devio-image/main/whisper-trial-japanese/img/whisper-trial-japanese_2022-09-22-21-53-13.png)

## 参考サイト

- [OpenAIリリースのWhisperで文字起こし後にテキスト読み上げした話](https://dev.classmethod.jp/articles/transform-whisper-txt-into-audio-file/)  
- [OpenAI Whisper のコマンドオプション - Qiita](https://qiita.com/szktmyk38f/items/374f24d06fe277a1922a)  
- [WhisperのREADME](https://zenn.dev/piment/articles/ca917d0e9c8a49)  
- [DockerとDocker ComposeでPythonの実行環境を作成する | ZUMA Lab](https://zuma-lab.com/posts/docker-python-settings)  
- [OpenAIがリリースした高精度な音声認識モデル”Whisper”を使って、オンライン会議の音声を書き起こししてみた | DevelopersIO](https://dev.classmethod.jp/articles/whisper-trial-japanese/)  
