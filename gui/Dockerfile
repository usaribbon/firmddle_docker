FROM dorowu/ubuntu-desktop-lxde-vnc

RUN mkdir /root/firmusa/
RUN wget https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_10.1.5_build/ghidra_10.1.5_PUBLIC_20220726.zip -O /root/firmusa/ghidra_10.1.5_PUBLIC_20220726.zip
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
RUN apt-get update && apt-get install -y zip unzip
RUN unzip /root/firmusa/ghidra_10.1.5_PUBLIC_20220726.zip -d /root/firmusa/
RUN apt-get install -y openjdk-11-jdk openjdk-11-jre make gcc g++
RUN echo 'PATH="$PATH:/usr/lib/jvm/java-11-openjdk-amd64/bin"' >> /root/.bashrc

RUN apt-get install -y git zlib1g-dev liblzma-dev liblzo2-dev p7zip-full squashfs-tools file
RUN mkdir /root/firmusa/tmp
RUN cd /root/firmusa/tmp
RUN git clone https://github.com/usaribbon/sasquatch.git
RUN echo 'export PATH=$PATH:/root/firmusa/firmware-mod-kit/src/squashfs-3.0/' >> /root/.bashrc
RUN cd sasquatch && ./build.sh
RUN cd /root/firmusa/
RUN git clone https://github.com/usaribbon/firmddle-ghidrascript.git
RUN git clone https://github.com/usaribbon/firmware-mod-kit.git
RUN chmod +x /root/firmware-mod-kit/extract_elf.sh
RUN chmod +x /root/firmware-mod-kit/import_elf_ghidra.sh
RUN chmod +x /root/firmware-mod-kit/src/binwalk-2.1.1/src/scripts/binwalk

RUN mkdir /root/eclipse
COPY raw_firmwares/eclipse/* /root/eclipse/
RUN tar xfz /root/eclipse/eclipse-committers-2022-06-R-linux-gtk-x86_64.tar.gz 

RUN mkdir /root/ghidra_scripts
RUN cp /root/firmddle-ghidrascript/* /root/ghidra_scripts/