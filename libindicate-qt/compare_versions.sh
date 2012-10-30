#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' libindicate-qt.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_match_rel[ ]*\(.*\)$/\1/p' libindicate-qt.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q -O - 'https://launchpad.net/ubuntu/quantal/+source/libindicate-qt' | sed -n 's/^.*current\ release\ (\(.*\)-\(.*\)).*$/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/libindicate-qt/+download' -O - | sed -n 's/.*libindicate-qt-\(.*\)\.tar\.bz2.*/\1/p' | head -n 1)

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
