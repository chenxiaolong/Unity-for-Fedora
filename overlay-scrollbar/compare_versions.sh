#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' overlay-scrollbar.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' overlay-scrollbar.spec)"
BZR_REV="$(sed -n 's/^%define[ ]*_bzr_rev[ ]*\(.*\)$/\1/p' overlay-scrollbar.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q -O - 'https://launchpad.net/ubuntu/quantal/+source/overlay-scrollbar' | sed -n 's/^.*current\ release\ (\(.*\)-\(.*\)).*$/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/ayatana-scrollbar/+download' -O - | sed -n 's/.*overlay-scrollbar-\(.*\)\.tar\.gz.*/\1/p' | head -n 1)

echo ""

echo -e "spec file version: ${SPEC_VER}+r${BZR_REV} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
