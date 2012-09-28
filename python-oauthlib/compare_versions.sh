#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' python-oauthlib.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' python-oauthlib.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/quantal/source/python-oauthlib' -O - | sed -n 's/.*>python-oauthlib_\(.*\)-\(.*\)\.debian\.tar\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'http://pypi.python.org/pypi/oauthlib' -O - | sed -n 's/.*>oauthlib-\(.*\)\.tar\.gz<.*/\1/p' | head -1)

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
