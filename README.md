# マニュアル / Documentation
The English version is written after Japanese version.

# 環境構築

1. dockerをインストールし、`docker`と`docker-compose`コマンドが使えることを確認してください。
  * https://www.docker.com/products/docker-desktop/
2. eclipseを以下のURLからダウンロードしてください。
  * https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/2022-06/R/eclipse-committers-2022-06-R-linux-gtk-x86_64.tar.gz
3. 以下のURLからこのgitリポジトリをダウンロードしてください。
  * https://github.com/usaribbon/firmddle_docker/archive/refs/heads/main.zip
  * もしくは`git clone https://github.com/usaribbon/firmddle_docker.git`
4. 先程ダウンロードしたeclipseのtar.gzファイルを、firmddle_docker/raw_firmwares/eclipse/のディレクトリにコピーしてください。
5. ダウンロードしたgitリポジトリに移動し、以下のようなディレクトリ構造になっていることを確認してください。
```
.
├── docker-compose.yml
├── gui
│   └── Dockerfile
└── raw_firmwares   ←docker上では/mnt/raw_firmwares/としてマウントされます
    ├── eclipse
    │   └── eclipse-committers-2022-06-R-linux-gtk-x86_64.tar.gz
    ├── elf
    ├── extracted
    ├── ghidraprj
    ├── raw
```
6. gitリポジトリ内で以下のコマンドを実行し、dockerをビルド＆起動させてください。
  ```
  docker-compose build
  docker-compose up -d
  ```
  * (Windows)iptablesの関係でStep7,9で初回ビルドは失敗してしまいます。その際はdockerを再起動して、もう一度ビルドコマンドを実行してみてください。

7. ホストPCのWEBブラウザから`http://127.0.0.1:8080/`にアクセスしてdockerコンテナに入ってください。（環境によって接続までに数分〜数十分かかる場合があります）
  ![docker](https://user-images.githubusercontent.com/2094358/193526468-df754d54-5979-439d-b004-5de2ee806302.png)
8. ファイルマネージャーから`/root/firmusa/ghidra_10.1.5_PUBLIC_20220726/ghidraRun`にアクセスし、Ghidraを起動してください。
  ![docker](https://user-images.githubusercontent.com/2094358/193527140-b074dc9c-6243-42c9-b458-4cf1d3ec6b8e.png)
　 


# ファームウェアを分割する
1. 分割したいファームウェアを、gitリポジトリのraw_firmwares/raw/に置いてください。dockerには/mnt/raw_firmwares/としてマウントされています。
1. docker上で`/root/firmware-mod-kit/extract_elf.sh`　を実行してください。/mnt/raw_firmwares/に置かれているファームウェアの分割が始まります。
1. 分割されたファームウェアは、/mnt/raw_firmwares/extracted/に置かれます。

# Ghidraにファームウェアをインポートする
1. 「ファームウェアを分割する」の手順を実行した後、`/root/firmware-mod-kit/import_elf_ghidra.sh`　を実行してください。
1. 分割したファームウェアがGhidraにインポートされていきます。ファームウェアのサイズが大きい場合、インポートに時間がかかる場合があります。
1. ファームウェアごとにGhidraプロジェクトが作成され、/mnt/raw_firmwares/ghidraprj/に保存されます。
1. ファイルマネージャーから`/root/firmusa/ghidra_10.1.5_PUBLIC_20220726/ghidraRun`にアクセスし、Ghidraを起動してください。
1. Ghidraから、File -> Open Projectを選択して`/mnt/raw_firmwares/ghidraprj/好きなファームウェア名.gpr`を開きます。

###  （おまけ）Ghidraで新規プロジェクトを作成してELFをインポートする
1. /root/firmusa/ghidra_10.1.5_PUBLIC_20220726/ghidraRun を実行してGhidraを起動してください。
2. NewProjectを選択します。
<img width="799" alt="スクリーンショット 2022-10-03 17 02 24" src="https://user-images.githubusercontent.com/2094358/193529640-51a17312-cf7f-4bd0-bc63-ecfa6b143030.png">
3. Non-Shared Projectを選択します。
<img width="670" alt="スクリーンショット 2022-10-03 17 02 31" src="https://user-images.githubusercontent.com/2094358/193529639-d7445ae5-359a-479f-ad40-86067eec3906.png">
4. プロジェクトの保存先を指定します。
<img width="671" alt="スクリーンショット 2022-10-17 19 09 52" src="https://user-images.githubusercontent.com/2094358/196151437-ca11d187-7b10-4874-bcae-5230d1789449.png">
5. Import Fileを選択します。
<img width="796" alt="スクリーンショット 2022-10-03 17 04 10" src="https://user-images.githubusercontent.com/2094358/193529630-6f8c1445-0ba0-4397-8030-736604da148f.png">
6. 読み込ませるELFファイルを指定します。
<img width="794" alt="スクリーンショット 2022-10-03 17 05 26" src="https://user-images.githubusercontent.com/2094358/193529628-dae23b42-d971-4e60-a48f-3e8349b78e4d.png">
7. OKを選択します。
<img width="501" alt="スクリーンショット 2022-10-03 17 05 32" src="https://user-images.githubusercontent.com/2094358/193529626-93dcebc9-32bb-4b4e-95a1-9d6024fb1ed0.png">
8. OKを選択します。
<img width="802" alt="スクリーンショット 2022-10-03 17 05 41" src="https://user-images.githubusercontent.com/2094358/193529625-a4ff1b93-23aa-47b2-be27-2b0060841b18.png">
9. Yesを選択します。
<img width="1435" alt="スクリーンショット 2022-10-03 17 05 57" src="https://user-images.githubusercontent.com/2094358/193529623-8f2806e4-07c6-48c9-a4f9-6689b16482c6.png">
10. Analyzeを選択します。解析が完了するまでしばらく待ちます。
<img width="1006" alt="スクリーンショット 2022-10-03 17 06 05" src="https://user-images.githubusercontent.com/2094358/193529619-dfebeff7-2c26-42d2-af9c-15437848c8df.png">
11. プロジェクト画面の左上の「SAVE」ボタンを押して解析結果を保存します。
<img width="513" alt="スクリーンショット 2022-10-03 17 06 54" src="https://user-images.githubusercontent.com/2094358/193529614-c10bb0cb-5da6-4f2f-ad89-948165df6b8d.png">

# HeadlessAnalyzerの使い方
* プロジェクト内の全ファイルに対してスクリプトを適用したいときは、下記のコマンドを実行してください
`/root/firmusa/ghidra_10.1.5_PUBLIC/support/analyzeHeadless /mnt/raw_firmwares/ghidraprj binary2 -scriptPath /root/ghidra_scripts -postScript Yoda_API_Headless.java -process -recursive`
* スクリプトを適用した結果は、dockerの`/mnt/raw_firmwares/logs/`、またはホストPCの`このgitリポジトリ/raw_firmwares/logs/`に保存されています。



# Setup

1. Install docker and make sure `docker` and `docker-compose` commands are available.
  * https://www.docker.com/products/docker-desktop/
2. Download eclipse from the following URL
  * https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/2022-06/R/eclipse-committers-2022-06-R-linux-gtk-x86_64.tar.gz
3. Download this git repository from the following URL
  * https://github.com/usaribbon/firmddle_docker/archive/refs/heads/main.zip
  * Or `git clone https://github.com/usaribbon/firmddle_docker.git`
4. Copy the eclipse tar.gz file you just downloaded to the directory firmddle_docker/raw_firmwares/eclipse/
5. Go to the git repository you downloaded and make sure the directory structure looks like this
```
.
├── docker-compose.yml
├── gui
│   └── Dockerfile
└── raw_firmwares   ←mounted as /mnt/raw_firmwares/ on docker
    ├── eclipse
    │   └── eclipse-committers-2022-06-R-linux-gtk-x86_64.tar.gz
    ├── elf
    ├── extracted
    ├── ghidraprj
    ├── raw
```
6. Execute the following command in the git repository to build and start docker.
  ```
  docker-compose build
  docker-compose up -d
  ```
  * (Windows) Due to iptables, the first build will fail in Step 7 and 9. In that case, restart docker and run the build command again.

7. Please access `http://127.0.0.1:8080/` from a web browser on the host PC to enter the docker container. (It may take several minutes to several tens of minutes to connect depending on the environment.) 
  ![docker](https://user-images.githubusercontent.com/2094358/193526468-df754d54-5979-439d-b004-5de2ee806302.png)
8. Access `/root/firmusa/ghidra_10.1.5_PUBLIC_20220726/ghidraRun` from the file manager and start Ghidra.
  ![docker](https://user-images.githubusercontent.com/2094358/193527140-b074dc9c-6243-42c9-b458-4cf1d3ec6b8e.png)

# Split the firmware
1. Place the firmware you want to split in the git repository raw_firmwares/raw/. docker has it mounted as /mnt/raw_firmwares/
1. Run `/root/firmware-mod-kit/extract_elf.sh` on docker. The firmware placed in /mnt/raw_firmwares/ will start to be split.
1. The split firmware will be placed in /mnt/raw_firmwares/extracted/

# Importing firmware into Ghidra
1. After performing the steps in "Splitting Firmware," run `/root/firmware-mod-kit/import_elf_ghidra.sh`.
1. The split firmware will be imported into Ghidra. If the firmware is large, the import may take some time.
1. A Ghidra project will be created for each firmware and saved in /mnt/raw_firmwares/ghidraprj/.
1. Access `/root/firmusa/ghidra_10.1.5_PUBLIC_20220726/ghidraRun` from the file manager and start Ghidra.
`. From Ghidra, select File -> Open Project and open `/mnt/raw_firmwares/ghidraprj/firmware_name.gpr` of your choice.

###  (extra) Create a new project in Ghidra and import the ELF
1. Run Ghidra by executing `/root/firmusa/ghidra_10.1.5_PUBLIC_20220726/ghidraRun`
2. Select NewProject.
<img width="799" alt="スクリーンショット 2022-10-03 17 02 24" src="https://user-images.githubusercontent.com/2094358/193529640-51a17312-cf7f-4bd0-bc63-ecfa6b143030.png">
3. Select Non-Shared Project
<img width="670" alt="スクリーンショット 2022-10-03 17 02 31" src="https://user-images.githubusercontent.com/2094358/193529639-d7445ae5-359a-479f-ad40-86067eec3906.png">
4. Choose a folder to save your project.
<img width="671" alt="スクリーンショット 2022-10-17 19 09 52" src="https://user-images.githubusercontent.com/2094358/196151437-ca11d187-7b10-4874-bcae-5230d1789449.png">
5. Select Import File
<img width="796" alt="スクリーンショット 2022-10-03 17 04 10" src="https://user-images.githubusercontent.com/2094358/193529630-6f8c1445-0ba0-4397-8030-736604da148f.png">
6. Select ELF files
<img width="794" alt="スクリーンショット 2022-10-03 17 05 26" src="https://user-images.githubusercontent.com/2094358/193529628-dae23b42-d971-4e60-a48f-3e8349b78e4d.png">
7. Select OK
<img width="501" alt="スクリーンショット 2022-10-03 17 05 32" src="https://user-images.githubusercontent.com/2094358/193529626-93dcebc9-32bb-4b4e-95a1-9d6024fb1ed0.png">
8. Select OK
<img width="802" alt="スクリーンショット 2022-10-03 17 05 41" src="https://user-images.githubusercontent.com/2094358/193529625-a4ff1b93-23aa-47b2-be27-2b0060841b18.png">
9. Select Yes。
<img width="1435" alt="スクリーンショット 2022-10-03 17 05 57" src="https://user-images.githubusercontent.com/2094358/193529623-8f2806e4-07c6-48c9-a4f9-6689b16482c6.png">
10. Select Analyze. Wait a moment for the analysis to complete.
<img width="1006" alt="スクリーンショット 2022-10-03 17 06 05" src="https://user-images.githubusercontent.com/2094358/193529619-dfebeff7-2c26-42d2-af9c-15437848c8df.png">
11. Save the analysis results by pressing the "SAVE" button in the upper left corner of the project screen.
<img width="513" alt="スクリーンショット 2022-10-03 17 06 54" src="https://user-images.githubusercontent.com/2094358/193529614-c10bb0cb-5da6-4f2f-ad89-948165df6b8d.png">

# How to use HeadlessAnalyzer
* If you want to apply the script to all files in the project, run the following command
`/root/firmusa/ghidra_10.1.5_PUBLIC/support/analyzeHeadless /mnt/raw_firmwares/ghidraprj binary2 -scriptPath /root/ghidra_scripts - postScript Yoda_API_Headless.java -process -recursive`.
* The results of applying the scripts are stored in `/mnt/raw_firmwares/logs/` on docker or in `this git repository/raw_firmwares/logs/` on the host PC.
The results are stored in the host PC.
