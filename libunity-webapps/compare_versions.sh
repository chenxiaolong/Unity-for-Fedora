#!/usr/bin/env bash

F17_SPEC_VER="$(rpmspec -q --qf '%{version}\n' libunity-webapps-Fedora_17.spec | head -1)"
F18_SPEC_VER="$(rpmspec -q --qf '%{version}\n' libunity-webapps-Fedora_18.spec | head -1)"
F18_UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' libunity-webapps-Fedora_18.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q -O - 'https://launchpad.net/ubuntu/quantal/+source/libunity-webapps' | sed -n 's/^.*current\ release\ (\(.*\)-\(.*\)).*$/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/libunity-webapps/+download' -O - | sed -n 's/.*unity_webapps-\(.*\)\.tar\.gz.*/\1/p' | head -n 1)

echo ""

echo -e "F17 spec version: ${F17_SPEC_VER}"
echo -e "F18 spec version: ${F18_SPEC_VER} ${F18_UBUNTU_REL}"
echo -e "Upstream version: ${UPSTREAM_VER}"
echo -e "Ubuntu version:   ${UBUNTU_VER[@]}"
