#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=gtk3-ubuntu-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version: $(get_gnome_version gtk+ 3.6)"
echo -e "Ubuntu version:   $(get_ubuntu_version gtk+3.0 ${1:-raring})"
