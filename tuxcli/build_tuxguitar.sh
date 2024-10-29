#!/bin/bash

cd tuxbuild

# Install prerequisites
sudo apt install -y wget unzip git build-essential default-jdk maven libwebkit2gtk-4.1-0 libfluidsynth-dev libjack-jackd2-dev libasound2-dev liblilv-dev libsuil-dev qtbase5-dev fonts-wqy-zenhei

# Download and install SWT for Linux
SWT_ZIP="swt-4.26-gtk-linux-$(uname -m).zip"
SWT_DIR="swt-4.26-gtk-linux-$(uname -m)"
wget "https://archive.eclipse.org/eclipse/downloads/drops4/R-4.26-202211231800/$SWT_ZIP"
mkdir $SWT_DIR
cd $SWT_DIR
unzip "../$SWT_ZIP"
mvn install:install-file -Dfile=swt.jar -DgroupId=org.eclipse.swt -DartifactId=org.eclipse.swt.gtk.linux -Dpackaging=jar -Dversion=4.26
cd ..

# Get the TuxGuitar sources
git clone https://github.com/helge17/tuxguitar.git
cd tuxguitar

# Build and install
cd desktop/build-scripts/tuxguitar-linux-swt-deb
mvn -e clean verify -P native-modules
sudo dpkg -i target/tuxguitar-*.deb
