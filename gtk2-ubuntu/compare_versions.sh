#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=gtk2-ubuntu-Fedora_17.spec
echo -e "F17 spec version: $(get_spec_version) $(get_spec_release --ubuntu)"
SPECFILE=gtk2-ubuntu-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version: $(get_gnome_version gtk+ 2.24)"
echo -e "Ubuntu version:   $(get_ubuntu_version gtk+2.0 ${1:-raring})"
