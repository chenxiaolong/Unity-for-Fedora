#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' libqtgconf.spec | head -1)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise/source/libqtgconf' -O - | sed -n 's/.*>libqtgconf_\(.*\)-\(.*\)\.debian\.tar\.gz<.*/\1 \2/p'))

echo ""

echo -e "spec file version: ${SPEC_VER}"
echo -e "Upstream version:  (none)"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
