#!/usr/bin/env bash

F17_SPEC_VER="$(rpmspec -q --qf '%{version}\n' indicator-messages-Fedora_17.spec | head -1)"
F18_SPEC_VER="$(rpmspec -q --qf '%{version}\n' indicator-messages-Fedora_18.spec | head -1)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/quantal/source/indicator-messages' -O - | sed -n 's/.*>indicator-messages_\(.*\)-\(.*\)\.diff\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/indicator-messages/+download' -O - | sed -n 's/.*indicator-messages-\(.*\)\.tar\.gz.*/\1/p' | head -n 1)

echo ""

echo -e "F17 spec version: ${F17_SPEC_VER}"
echo -e "F18 spec version: ${F18_SPEC_VER}"
echo -e "Upstream version: ${UPSTREAM_VER}"
echo -e "Ubuntu version:   ${UBUNTU_VER[@]}"
