#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' compiz.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' compiz.spec)"
BZR_REV="$(sed -n 's/^%define[ ]*_bzr_rev[ ]*\(.*\)$/\1/p' compiz.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/quantal/source/compiz' -O - | sed -n 's/.*>compiz_\(.*\)-\(.*\)\.diff\.gz<.*/\1 \2/p'))

echo ""

echo -e "spec file version: ${SPEC_VER}+bzr${BZR_REV} ${UBUNTU_REL}"
echo -e "Upstream version:  (none)"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
