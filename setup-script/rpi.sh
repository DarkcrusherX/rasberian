#!/bin/bash

# Use etcher to balena etcher to flash ubuntu in rpi

# edit network-config in boot partition to add pwd and sshid of your wifi.
# ip -a to find my laptop ip
# nmap -sn <ip>
# trial and error all ip with ssh ubuntu@<ip>        xD
# you will get key gen error. Solve it as instructed.

# Login with pwd "ubuntu" and after tht u will be asked to change pwd

# apt install git and clone and run this script :" 

set -e

echo "*****************************************************************************"
echo
echo "Setup script to install ros melodic and zshrc"
echo
echo

read -p "Do you want to install zsh ? [y/n]: " tempvar

tempvar=${tempvar:-q}

if [ "$tempvar" = "y" ]; then
    echo "Removing any existing zsh thingies "
    rm -rf ~/.z*
    zsh_folder=/opt/.zsh/
    if [[ -d $zsh_folder ]];then
	    sudo rm -r /opt/.zsh/*
    fi
    echo
    echo "Installing zsh"
    echo
    sudo apt-get install zsh
    # chsh -s /usr/bin/zsh root
    sudo apt install wget git
    wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
    cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc

    source ~/.zshrc
    sudo apt-get install powerline fonts-powerline
    sudo apt-get install zsh-theme-powerlevel9k
    sudo apt-get install zsh-syntax-highlighting
    echo "source /usr/share/powerlevel9k/powerlevel9k.zsh-theme" >> ~/.zshrc
    echo "source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc
    sudo git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

read -p "Do you want to install ros melodic ? [y/n]: " tempvar

tempvar=${tempvar:-q}
if [ "$tempvar" = "y" ]; then

    sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
    sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
    sudo apt-get update
    sudo apt install -y python-rosdep python-rosinstall-generator python-wstool python-rosinstall build-essential cmake
    sudo rosdep init
    rosdep update
    sudo apt install ros-melodic-desktop