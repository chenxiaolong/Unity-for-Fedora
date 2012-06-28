#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' libappindicator.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_match_rel[ ]*\(.*\)$/\1/p' libappindicator.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise/source/libappindicator' -O - | sed -n 's/.*>libappindicator_\(.*\)-\(.*\)\.diff\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/libappindicator/+download' -O - | sed -n 's/.*libappindicator-\(.*\)\.tar\.gz.*/\1/p' | head -n 1)

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
