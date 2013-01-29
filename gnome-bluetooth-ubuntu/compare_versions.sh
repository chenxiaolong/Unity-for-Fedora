#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=gnome-bluetooth-ubuntu-Fedora_17.spec
echo -e "F17 spec version: $(get_spec_version) $(get_spec_release --ubuntu)"
SPECFILE=gnome-bluetooth-ubuntu-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version: $(get_gnome_version gnome-bluetooth 3.6)"
echo -e "Ubuntu version:   $(get_ubuntu_version gnome-bluetooth ${1:-raring})"
