#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' ccsm.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' ccsm.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise/source/compizconfig-settings-manager' -O - | sed -n 's/.*>compizconfig-settings-manager_\(.*\)-\(.*\)\.diff\.gz<.*/\1 \2/p'))

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  (none)"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
