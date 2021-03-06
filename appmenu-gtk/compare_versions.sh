#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=appmenu-gtk-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version appmenu-gtk)"
echo -e "Ubuntu version:   $(get_ubuntu_version appmenu-gtk ${1:-raring})"
