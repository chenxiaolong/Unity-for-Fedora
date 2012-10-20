#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' libtimezonemap.spec | head -1)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q -O - 'https://launchpad.net/ubuntu/quantal/+source/libtimezonemap' | sed -n 's/^.*current\ release\ (\(.*\)).*$/\1/p'))

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  (none)"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
