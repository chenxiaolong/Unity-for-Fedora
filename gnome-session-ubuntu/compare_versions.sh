#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=gnome-session-ubuntu-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version: $(get_gnome_version gnome-session 3.6)"
echo -e "Fedora version:   $(get_fedora_version gnome-session 18)"
echo -e "Ubuntu version:   $(get_ubuntu_version gnome-session ${1:-saucy})"
