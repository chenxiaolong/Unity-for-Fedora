#!/usr/bin/env bash

F17_SPEC_VER="$(rpmspec -q --qf '%{version}\n' libXfixes-ubuntu-Fedora_17.spec | head -1)"
F17_UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' libXfixes-ubuntu-Fedora_17.spec)"
F18_SPEC_VER="$(rpmspec -q --qf '%{version}\n' libXfixes-ubuntu-Fedora_18.spec | head -1)"
F18_UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' libXfixes-ubuntu-Fedora_18.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/quantal/source/libxfixes' -O - | sed -n 's/.*>libxfixes_\(.*\)-\(.*\)\.diff\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q http://xorg.freedesktop.org/releases/individual/lib/ -O - | sed -n 's/.*libXfixes-\(.*\).tar.bz2.*/\1/p' | tail -n 1)

echo ""

echo -e "F17 spec version: ${F17_SPEC_VER} ${F17_UBUNTU_REL}"
echo -e "F18 spec version: ${F18_SPEC_VER} ${F18_UBUNTU_REL}"
echo -e "Upstream version: ${UPSTREAM_VER}"
echo -e "Ubuntu version:   ${UBUNTU_VER[@]}"
