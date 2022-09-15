# マニュアル

# 環境構築

1. dockerをインストールしてください。https://www.docker.com/products/docker-desktop/
1. eclipseをダウンロードしてください。https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/2022-06/R/eclipse-committers-2022-06-R-linux-gtk-x86_64.tar.gz
1. https://github.com/usaribbon/firmddle_docker　から、リポジトリのZIPファイルをダウンロードしてください。
　もしくは、git clone https://github.com/usaribbon/firmddle_docker.git
1. ダウンロードしたリポジトリに移動してください。
1. ダウンロードしたeclipseのtar.gzファイルを、firmddle_docker/raw_firmwares/eclipse/のディレクトリにコピーしてください。
1. 以下のコマンドを実行し、dockerをビルド＆起動させてください。
  ```
  docker-compose build
  docker-compose up -d
  ```
1. http://127.0.0.1:8080/　にアクセスしてdockerコンテナに入る
1. ./ghidra_10.1.5_PUBLIC/ghidraRun

## ファームウェアを分割する
```
.
├── docker-compose.yml
├── gui
│   └── Dockerfile
└── raw_firmwares
    ├── eclipse
    │   └── eclipse-committers-2022-06-R-linux-gtk-x86_64.tar.gz
    ├── elf
    ├── extracted
    ├── ghidraprj
    ├── raw
    │   └── test.bin
```
1. 分割したいファームウェアは、リポジトリのraw_firmwares/raw/に置いてください。dockerには/mnt/raw_firmwares/にマウントされています。
1. docker上で`/root/firmware-mod-kit/extract_elf.sh`　を実行してください。ファームウェアの分割が始まります。
1. 分割されたファームウェアは、/mnt/raw_firmwares/extracted/に置かれます。
1. 分割されたファームウェアのうち、Ghidraが読み込めるELFのリストは、/mnt/raw_firmwares/elf/に置かれます。このelfファイルをGhiraに読み込ませます。

## ELFファイルをGhiraにインポートする
### docker上でGhidraが起動する場合
1. /root/firmusa/ghidra_10.1.5_PUBLIC_20220726/ghidraRun を実行してGhidraを起動してください。
1. Ghidra起動後のマニュアルをご参照ください

### docker上でGhidraが起動しない場合
1. ホストPCにGhidraをダウンロードしてください。https://ghidra-sre.org/
1. Java JDK11（以上）とJRE11（以上）をインストールしてください。
1. ダウンロードしたGhidraのディレクトリから、`ghidraRun`　を実行してGhidraを起動してください。
1. firmddle_dockerリポジトリのディレクトリに移動してください。
1. ターミナルから`./firmddle_dockerリポジトリ/script_bash/import_ghidra_hostpc.sh "Ghidraのディレクトリ場所"`を実行してください。
1. firmddle_dockerリポジトリ/raw_firmwares/ghidraprj/に、各ファームウェアごとのGhidraが生成されています。
1. `docker cp ubuntu-gui:/root/firmddle-ghidrascript/  firmddle_dockerリポジトリ/` ghidraのスクリプト
1. GhidraのスクリプトをGhidraにインポートします


## Ghidraのスクリプトをプロジェクト内のすべてのELFファイルに適用する
/GHIDRAのディレクトリ/ghidra_10.1.2_PUBLIC/support/analyzeHeadless.bat ${プロジェクトが格納されている上位ディレクトリ} ${プロジェクト名} -scriptPath /SCRIPTパス/ghidra_scripts -postScript スクリプト名.java -import ${ELFパス} -overwrite

## Ghidraのスクリプトをプロジェクト内のすべてのELFファイルに適用する
/GHIDRAのディレクトリ/ghidra_10.1.2_PUBLIC/support/analyzeHeadless.bat ${プロジェクトが格納されている上位ディレクトリ} ${プロジェクト名} -scriptPath /SCRIPTパス/ghidra_scripts -postScript スクリプト名.java -import ${ELFパス} -overwrite
