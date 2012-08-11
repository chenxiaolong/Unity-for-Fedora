#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' plasma-widget-menubar.spec | head -1)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/quantal/source/plasma-widget-menubar' -O - | sed -n 's/.*>plasma-widget-menubar_\(.*\)-\(.*\)\.debian\.tar\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/plasma-widget-menubar/+download' -O - | sed -n 's/.*plasma-widget-menubar-\(.*\)\.tar\.bz2.*/\1/p' | head -n 1)

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"