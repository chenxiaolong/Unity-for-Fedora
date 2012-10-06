#!/usr/bin/env bash

F17_SPEC_VER="$(rpmspec -q --qf '%{version}\n' libunity-webapps-Fedora_17.spec | head -1)"
F18_SPEC_VER="$(rpmspec -q --qf '%{version}\n' libunity-webapps-Fedora_18.spec | head -1)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/quantal/source/libunity-webapps' -O - | sed -n 's/.*>libunity-webapps_\(.*\)-\(.*\)\.debian\.tar\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/libunity-webapps/+download' -O - | sed -n 's/.*unity_webapps-\(.*\)\.tar\.gz.*/\1/p' | head -n 1)

echo ""

echo -e "F17 spec version: ${F17_SPEC_VER}"
echo -e "F18 spec version: ${F18_SPEC_VER}"
echo -e "Upstream version: ${UPSTREAM_VER}"
echo -e "Ubuntu version:   ${UBUNTU_VER[@]}"
