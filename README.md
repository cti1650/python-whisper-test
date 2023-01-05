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
      > イスタンブールは世界で唯一アジア大陸とヨーロッパ大陸にまたがる街で、この2つの大陸を分けているのがボスポラス海峡です。アジアとヨーロッパの間を進んでいく、壮大な体験ができる、ボスポラス海峡クルーズを堪能していただく予定です。

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
- [Python - ディクショナリーの初期化、4つの方法](https://codechacha.com/ja/python-initialize-dict/#3-fromkeys-%E3%81%A7%E8%BE%9E%E6%9B%B8%E3%82%92%E5%88%9D%E6%9C%9F%E5%8C%96%E3%81%99%E3%82%8B)  
- [Pythonでリスト（配列）に要素を追加するappend, extend, insert | note.nkmk.me](https://note.nkmk.me/python-list-append-extend-insert/)  
- [Python の time で時間を計測する。 | 民主主義に乾杯](https://python.ms/time/#_1-%E4%BD%BF%E3%81%84%E6%96%B9-%E3%81%9D%E3%81%AE1)  
