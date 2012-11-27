#!/usr/bin/env bash

F18_SPEC_VER="$(rpmspec -q --qf '%{version}\n' indicator-power-Fedora_18.spec | head -1)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q -O - 'https://launchpad.net/ubuntu/raring/+source/indicator-power' | sed -n 's/^.*current\ release\ (\(.*\)-\(.*\)).*$/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/indicator-power/+download' -O - | sed -n 's/.*indicator-power-\(.*\)\.tar\.gz.*/\1/p' | head -n 1)

echo ""

echo -e "F18 spec version: ${F18_SPEC_VER}"
echo -e "Upstream version: ${UPSTREAM_VER}"
echo -e "Ubuntu version:   ${UBUNTU_VER[@]}"
