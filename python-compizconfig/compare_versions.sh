#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' python-compizconfig.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' python-compizconfig.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise/source/compizconfig-python' -O - | sed -n 's/.*>compizconfig-python_\(.*\)-\(.*\)\.diff\.gz<.*/\1 \2/p'))

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  (none)"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
