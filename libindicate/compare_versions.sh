#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' libindicate.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_match_rel[ ]*\(.*\)$/\1/p' libindicate.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise/source/libindicate' -O - | sed -n 's/.*>libindicate_\(.*\)-\(.*\)\.diff\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/libindicate/+download' -O - | sed -n 's/.*libindicate-\(.*\)\.tar\.gz.*/\1/p' | head -n 1)

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
