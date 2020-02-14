#!/bin/bash
echo "Installer for cpp-accounting"
echo "Please make sure that following dependencies are installed & updated:"
echo "git, make, cmake, build-essential, qtbase5-dev, qt5-default, libqt5charts5-dev"

echo $'\n\n----------- FETCH JSONCPP SUBMODULE -----------'
git submodule update --init --recursive

echo $'\n\n----------- BUILD JSONCPP -----------'
cd src/jsoncpp
mkdir -p build/debug
cd build/debug
cmake -DCMAKE_BUILD_TYPE=debug -DBUILD_STATIC_LIBS=ON -DBUILD_SHARED_LIBS=OFF -DARCHIVE_INSTALL_DIR=. -G "Unix Makefiles" ../..
make

echo $'\n\n----------- BUILD CORE BINARIES -----------'
cd ../../.. # back to src
make

echo $'\n\n----------- BUILD GUI & COPY EXAMPLE DATASET -------------'
cd gui
qmake
make

cd .. # back to root
cp -r ../doc/example_dataset data # copy example dataset

echo $'\n\nBuilding complete. Program can be run with:'
echo "./gui in src/gui for GUI"
echo "./main in src/ for main"
echo "./test in test/ for GCheck tests"