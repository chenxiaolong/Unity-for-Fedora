#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=xorg-x11-proto-ubuntu-devel-Fedora_17.spec
echo -e "F17 real spec version: $(get_spec_version) $(get_spec_define _fedora_rel)"
echo -e "F17 spec file version: $(get_spec_define _ver_fixesproto) $(get_spec_release --ubuntu)"
echo -e "F17 Fedora version:    $(get_fedora_version xorg-x11-proto-devel 17)"
SPECFILE=xorg-x11-proto-ubuntu-devel-Fedora_18.spec
echo -e "F18 real spec version: $(get_spec_version) $(get_spec_define _fedora_rel)"
echo -e "F18 spec file version: $(get_spec_define _ver_fixesproto) $(get_spec_release --ubuntu)"
echo -e "F18 Fedora version:    $(get_fedora_version xorg-x11-proto-devel 18)"
echo -e "Upstream version:      $(get_xorg_version fixesproto proto)"
echo -e "Ubuntu version:        $(get_ubuntu_version x11proto-fixes ${1:-raring})"
