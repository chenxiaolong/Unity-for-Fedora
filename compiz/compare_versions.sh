#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' compiz.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' compiz.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise-updates/source/compiz' -O - | sed -n 's/.*>compiz_\(.*\)-\(.*\)\.debian\.tar\.gz<.*/\1 \2/p'))

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  (none)"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
