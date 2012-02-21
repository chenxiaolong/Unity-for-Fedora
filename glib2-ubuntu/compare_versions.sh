#!/usr/bin/env bash

SPEC_VER="$(rpm --specfile glib2-ubuntu.spec -q --qf '%{version}\n' | head -n 1)"
UBUNTU_REL="$(cat glib2-ubuntu.spec | grep 'define.*_ubuntu_rel' | awk '{print $3}')"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise/source/glib2.0' -O - | sed -n 's/.*>glib2.0_\(.*\)-\(.*\)\.debian\.tar\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q "http://ftp.gnome.org/pub/GNOME/sources/glib/${SPEC_VER%.*}/" -O - | sed -n 's/.*>LATEST-IS-\(.*\)<.*/\1/p')

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
