#!/usr/bin/env bash

F17_SPEC_VER="$(rpmspec -q --qf '%{version}\n' gnome-screensaver-ubuntu-Fedora_17.spec | head -1)"
F17_UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' gnome-screensaver-ubuntu-Fedora_17.spec)"
F18_SPEC_VER="$(rpmspec -q --qf '%{version}\n' gnome-screensaver-ubuntu-Fedora_18.spec | head -1)"
F18_UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' gnome-screensaver-ubuntu-Fedora_18.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/quantal/source/gnome-screensaver' -O - | sed -n 's/.*>gnome-screensaver_\(.*\)-\(.*\)\.debian\.tar\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q "http://ftp.gnome.org/pub/GNOME/sources/gnome-screensaver/3.6/" -O - | sed -n 's/.*>LATEST-IS-\(.*\)<.*/\1/p')

echo ""

echo -e "F17 spec version: ${F17_SPEC_VER} ${F17_UBUNTU_REL}"
echo -e "F18 spec version: ${F18_SPEC_VER} ${F18_UBUNTU_REL}"
echo -e "Upstream version: ${UPSTREAM_VER}"
echo -e "Ubuntu version:   ${UBUNTU_VER[@]}"
