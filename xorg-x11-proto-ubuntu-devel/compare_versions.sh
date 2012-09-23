#!/usr/bin/env bash

F17_SPEC_VER="$(sed -n 's/^%define[ \t]*_ver_fixesproto[ \t]*\(.*\)$/\1/p' xorg-x11-proto-ubuntu-devel-Fedora_17.spec)"
F17_UBUNTU_REL="$(sed -n 's/^%define[ \t]*_ubuntu_rel[ \t]*\(.*\)$/\1/p' xorg-x11-proto-ubuntu-devel-Fedora_17.spec)"
F17_SPEC_REAL_VER="$(rpmspec -q --qf '%{version}\n' xorg-x11-proto-ubuntu-devel-Fedora_17.spec | head -1)"
F17_SPEC_FCREL="$(sed -n 's/^%define[ \t]*_fedora_rel[ \t]*\(.*\)$/\1/p' xorg-x11-proto-ubuntu-devel-Fedora_17.spec)"
F18_SPEC_VER="$(sed -n 's/^%define[ \t]*_ver_fixesproto[ \t]*\(.*\)$/\1/p' xorg-x11-proto-ubuntu-devel-Fedora_18.spec)"
F18_UBUNTU_REL="$(sed -n 's/^%define[ \t]*_ubuntu_rel[ \t]*\(.*\)$/\1/p' xorg-x11-proto-ubuntu-devel-Fedora_18.spec)"
F18_SPEC_REAL_VER="$(rpmspec -q --qf '%{version}\n' xorg-x11-proto-ubuntu-devel-Fedora_18.spec | head -1)"
F18_SPEC_FCREL="$(sed -n 's/^%define[ \t]*_fedora_rel[ \t]*\(.*\)$/\1/p' xorg-x11-proto-ubuntu-devel-Fedora_18.spec)"

echo "Getting latest Ubuntu version..."
UBUNTU_VER=($(wget -q 'http://packages.ubuntu.com/quantal/source/x11proto-fixes' -O - | sed -n 's/.*>x11proto-fixes_\(.*\)-\(.*\)\.diff\.gz<.*/\1 \2/p'))

echo "Getting latest Fedora version..."
FEDORA_VER="$(wget -q 'http://pkgs.fedoraproject.org/gitweb/?p=xorg-x11-proto-devel.git;a=blob_plain;f=xorg-x11-proto-devel.spec;hb=HEAD' -O tmp.spec && rpm -q --qf '%{version} %{release}' --specfile tmp.spec | sed 's/\.fc[0-9]*//' && rm tmp.spec)"

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q http://xorg.freedesktop.org/releases/individual/proto/ -O - | sed -n 's/.*fixesproto-\(.*\).tar.bz2.*/\1/p' | tail -n 1)

echo ""

echo -e "F17 real spec version: ${F17_SPEC_REAL_VER} ${F17_SPEC_FCREL}"
echo -e "F17 spec file version: ${F17_SPEC_VER} ${F17_UBUNTU_REL}"
echo -e "F18 real spec version: ${F18_SPEC_REAL_VER} ${F18_SPEC_FCREL}"
echo -e "F18 spec file version: ${F18_SPEC_VER} ${F18_UBUNTU_REL}"
echo -e "F18 Fedora version:    ${FEDORA_VER}"
echo -e "Upstream version:      ${UPSTREAM_VER}"
echo -e "Ubuntu version:        ${UBUNTU_VER[@]}"
