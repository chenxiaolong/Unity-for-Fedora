#!/usr/bin/env bash

F17_SPEC_VER="$(rpmspec -q --qf '%{version}\n' gtk3-ubuntu-Fedora_17.spec | head -1)"
F18_SPEC_VER="$(rpmspec -q --qf '%{version}\n' gtk3-ubuntu-Fedora_18.spec | head -1)"
F17_UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' gtk3-ubuntu-Fedora_17.spec)"
F18_UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' gtk3-ubuntu-Fedora_18.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_1204_VER=($(wget -q -O - 'https://launchpad.net/ubuntu/precise/+source/gtk+3.0' | sed -n 's/^.*current\ release\ (\(.*\)-\(.*\)).*$/\1 \2/p'))

UBUNTU_1210_VER=($(wget -q -O - 'https://launchpad.net/ubuntu/raring/+source/gtk+3.0' | sed -n 's/^.*current\ release\ (\(.*\)-\(.*\)).*$/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q "http://ftp.gnome.org/pub/GNOME/sources/gtk+/3.6/" -O - | sed -n 's/.*>LATEST-IS-\(.*\)<.*/\1/p')

echo ""

echo -e "F17 spec version:     ${F17_SPEC_VER} ${F17_UBUNTU_REL}"
echo -e "F18 spec version:     ${F18_SPEC_VER} ${F18_UBUNTU_REL}"
echo -e "Upstream version:     ${UPSTREAM_VER}"
echo -e "Ubuntu 12.04 version: ${UBUNTU_1204_VER[@]}"
echo -e "Ubuntu 12.10 version: ${UBUNTU_1210_VER[@]}"
