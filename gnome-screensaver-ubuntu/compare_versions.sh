#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=gnome-screensaver-ubuntu-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version: $(get_gnome_version gnome-screensaver 3.6)"
echo -e "Fedora version:   $(get_fedora_version gnome-screensaver 18)"
echo -e "Ubuntu version:   $(get_ubuntu_version gnome-screensaver ${1:-raring})"
