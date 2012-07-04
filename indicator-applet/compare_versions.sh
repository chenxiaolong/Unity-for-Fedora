#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' indicator-applet.spec | head -1)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise/source/indicator-applet' -O - | sed -n 's/.*>indicator-applet_\(.*\)-\(.*\)\.diff\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/indicator-applet/+download' -O - | sed -n 's/.*indicator-applet-\(.*\)\.tar\.gz.*/\1/p' | head -n 1)

echo ""

echo -e "spec file version: ${SPEC_VER}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
