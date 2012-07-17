#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' NetworkManager-gnome-ubuntu.spec | head -1)"
UBUNTU_VER="$(sed -n 's/^%define[ \t]*_ubuntu_ver[ \t]*\(.*\)$/\1/p' NetworkManager-gnome-ubuntu.spec)"
UBUNTU_REL="$(sed -n 's/^%define[ \t]*_ubuntu_rel[ \t]*\(.*\)$/\1/p' NetworkManager-gnome-ubuntu.spec)"
SPEC_FCREL="$(sed -n 's/^%define[ \t]*_fedora_rel[ \t]*\(.*\)$/\1/p' NetworkManager-gnome-ubuntu.spec)"
GIT_DATE="$(sed -n 's/^%define[ \t]*_git_date[ \t]*\(.*\)$/\1/p' NetworkManager-gnome-ubuntu.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/precise/source/network-manager-applet' -O - | sed -n 's/.*>network-manager-applet_\(.*\)-\(.*\)\.debian\.tar\.gz<.*/\1 \2/p'))

echo "Getting latest Fedora version..."
FEDORA_VER="$(wget -q 'http://pkgs.fedoraproject.org/gitweb/?p=NetworkManager.git;a=blob_plain;f=NetworkManager.spec;hb=f17' -O tmp.spec && rpm -q --qf '%{version} %{release}\n' --specfile tmp.spec | sed 's/\.fc[0-9]*//' | head -n 1 && rm tmp.spec)"

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q "http://ftp.gnome.org/pub/GNOME/sources/network-manager-applet/0.9/" -O - | sed -n 's/.*>LATEST-IS-\(.*\)<.*/\1/p')

echo ""

echo -e "Fedora version:    ${FEDORA_VER}"
echo -e "spec file version: ${SPEC_VER} Fedora ${SPEC_FCREL}.git${GIT_DATE} Ubuntu ${UBUNTU_VER} ${UBUNTU_REL}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    ${UBUNTU_VER[@]}"
