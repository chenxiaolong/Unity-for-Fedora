#!/usr/bin/env bash

F17_SPEC_VER="$(rpmspec -q --qf '%{version}\n' gnome-settings-daemon-ubuntu-Fedora_17.spec | head -1)"
F18_SPEC_VER="$(rpmspec -q --qf '%{version}\n' gnome-settings-daemon-ubuntu-Fedora_18.spec | head -1)"
F17_UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' gnome-settings-daemon-ubuntu-Fedora_17.spec)"
F18_UBUNTU_VER="$(sed -n 's/^%define[ ]*_ubuntu_ver[ ]*\(.*\)$/\1/p' gnome-settings-daemon-ubuntu-Fedora_18.spec)"
F18_UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' gnome-settings-daemon-ubuntu-Fedora_18.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q -O - 'https://launchpad.net/ubuntu/quantal/+source/gnome-settings-daemon' | sed -n 's/^.*current\ release\ (\(.*\)-\(.*\)).*$/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q "http://ftp.gnome.org/pub/GNOME/sources/gnome-settings-daemon/3.6/" -O - | sed -n 's/.*>LATEST-IS-\(.*\)<.*/\1/p')

echo ""

echo -e "spec file version: ${F17_SPEC_VER} ${F17_UBUNTU_REL}"
echo -e "spec file version: ${F18_SPEC_VER} Ubuntu ${F18_UBUNTU_VER} ${F18_UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
