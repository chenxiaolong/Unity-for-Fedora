#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' libqtdee.spec | head -1)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/quantal/source/libqtdee' -O - | sed -n 's/.*>libqtdee_\(.*\)-\(.*\)\.diff\.gz<.*/\1 \2/p'))

echo ""

echo -e "spec file version: ${SPEC_VER}"
echo -e "Upstream version:  (none)"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
