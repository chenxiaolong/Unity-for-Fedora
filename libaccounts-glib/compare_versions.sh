#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' libaccounts-glib.spec | head -1)"
UBUNTU_REL="$(sed -n 's/^%define[ ]*_ubuntu_rel[ ]*\(.*\)$/\1/p' libaccounts-glib.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/quantal/source/libaccounts-glib' -O - | sed -n 's/.*>libaccounts-glib_\(.*\)-\(.*\)\.debian\.tar\.gz<.*/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q "https://code.google.com/p/accounts-sso/downloads/list" -O - | sed -n 's/.*libaccounts-glib-\(.*\)\.tar\.gz.*/\1/p' | head -n 1)

echo ""

echo -e "spec file version: ${SPEC_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"