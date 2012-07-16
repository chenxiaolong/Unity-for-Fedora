#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' gnome-control-center-ubuntu.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' gnome-control-center-ubuntu.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise-updates/source/gnome-control-center' -O - | sed -n 's/.*>gnome-control-center_\(.*\)-\(.*\)\.debian\.tar\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q "http://ftp.gnome.org/pub/GNOME/sources/gnome-control-center/3.4/" -O - | sed -n 's/.*>LATEST-IS-\(.*\)<.*/\1/p')

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
