#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' signon-plugin-oauth2.spec | head -1)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q -O - 'https://launchpad.net/ubuntu/raring/+source/signon-plugin-oauth2' | sed -n 's/^.*current\ release\ (\(.*\)-\(.*\)).*$/\1 \2/p'))

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q "https://code.google.com/p/accounts-sso/downloads/list" -O - | sed -n 's/.*signon-oauth2-\(.*\)\.tar\.bz2.*/\1/p' | head -n 1)

echo ""

echo -e "spec file version: ${SPEC_VER}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
