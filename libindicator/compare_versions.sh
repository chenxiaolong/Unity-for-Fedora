#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' libindicator.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_match_rel[ ]*\(.*\)$/\1/p' libindicator.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise/source/libindicator' -O - | sed -n 's/.*>libindicator_\(.*\)-\(.*\)\.diff\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/libindicator/+download' -O - | sed -n 's/.*libindicator-\(.*\)\.tar\.gz.*/\1/p' | head -n 1)

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
