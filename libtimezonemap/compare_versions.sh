#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' libtimezonemap.spec | head -1)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise/source/libtimezonemap' -O - | sed -n 's/.*>libtimezonemap_\(.*\)\.tar\.gz<.*/\1/p'))

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  (none)"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
