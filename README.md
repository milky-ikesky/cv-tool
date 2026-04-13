# 📸 CV-Tool（画像・動画前処理ツール）

## 📝 概要

`cv-tool`は、画像および動画の前処理を行うためのコマンドラインツールです。   
PythonとOpenCVをベースに実装しています。

### ✨ 主な機能

* ✂️ Crop（切り抜き）
* 📐 Resize（解像度変更）
* 💡 Brightness（明るさ調整）
* 🎨 Saturation（彩度調整）
* 🔄 Rotate 90°（回転）
* ↔️ Flip（垂直・水平反転）

※ 設定はYAMLファイルで一括管理します。

## 💻 動作環境

以下のPythonバージョンで動作確認しています。

* Python 3.11.x
* Python 3.12.x
* Python 3.13.x
* Python 3.14.x

## 🚀 インストール

### 1. 📦 リポジトリのクローン

```bash
git clone https://github.com/milky-ikesky/cv-tool.git
cd cv-tool
```

### 2. 🧪 Conda環境の作成

任意のPythonバージョンで環境を作成し、有効化します。

```bash
conda create -n cv314 python=3.14
conda activate cv314
```

### 3. 📚 依存関係のインストール

```bash
pip install -r requirements.txt
```

## 🛠️ 使用方法

### 💻 CLIモード（コマンドライン）

```bash
python main.py [-h] [-t {image,i,video,v}] [-p PATH] [-c CONFIG] [-o OUTPUT]
```

#### ⚙️ オプション

* `-t, --type` : データタイプ指定: 'image(i)' または 'video(v)' (デフォルト: 'image')
* `-p, --path` : 画像または動画ファイルの入力パス (デフォルト: './assets')
* `-c, --config` : 設定ファイルパス (デフォルト: './config.yaml')
* `-o, --output` : 出力ディレクトリパス (デフォルト: './result')

#### ▶️ 実行例

```bash
# 単一画像
python main.py -t image -p ./assets/teddybear.jpeg -c config.yaml -o ./result

# ディレクトリ内の画像
python main.py -t image -p ./assets/ -c config.yaml -o ./result

# 動画
python main.py -t video -p ./assets/asakusa.mp4 -c config.yaml -o ./result
```

### 🖥️　インタラクティブモード（対話式）

```bash
python main.py --interactive
```

#### ⚙️ オプション

* `set type <image|video|i|v>` : データタイプ指定: 'image(i)' または 'video(v)' (デフォルト: 'image')
* `set path <path>` : 画像または動画ファイルの入力パス (デフォルト: './assets')
* `set config <path>` : 設定ファイルパス (デフォルト: './config.yaml')
* `set output <path>` : 出力ディレクトリパス (デフォルト: './result')
* `run` : 前処理を実行
* `show` : 現在の設定を表示
* `help` : コマンド一覧を表示
* `exit` : インタラクティブモードを終了

#### ▶️ 実行例

```bash
# 画像
> set type image
> set path ./assets/teddybear.jpeg
> run
> exit

# 動画
> set type video
> set path ./assets/asakusa.mp4
> run
> exit
```

## 📂 出力仕様

元ファイルは上書きされません。

## ⚙️ 設定ファイル

`config.yaml`で前処理の内容を指定できます。
各処理には`enabled`フラグがあります。

```
true：処理を有効化
false：処理を無効化
```

必要な処理だけを有効にして、前処理を実行できます。

## 📏 開発ルール

### 🌱 ブランチ命名

以下の形式で作成します。

```
種別/Issue番号-内容
```

* ✨ feature/ : 機能追加
* 🐛 fix/ : バグ修正
* 🚑 hotfix/ : 緊急対応
