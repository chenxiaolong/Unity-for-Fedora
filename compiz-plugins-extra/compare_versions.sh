#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' compiz-plugins-extra.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_match_rel[ ]*\(.*\)$/\1/p' compiz-plugins-extra.spec)"
BZR_REV="$(sed -n 's/^%define[ ]*_bzr_rev[ ]*\(.*\)$/\1/p' compiz-plugins-extra.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise/source/compiz-plugins-extra' -O - | sed -n 's/.*>compiz-plugins-extra_\(.*\)-\(.*\)\.debian\.tar\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://launchpad.net/compiz-plugins-extra/+download' -O - | sed -n 's/.*compiz-plugins-extra-\(.*\)\.tar\.bz2.*/\1/p' | head -n 1)

echo ""

echo -e "spec file version: ${SPEC_VER}~bzr${BZR_REV} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
