#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=libXfixes-ubuntu-Fedora_18.spec
echo -e "F18 spec version:   $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "F18 Fedora version: $(get_fedora_version libXfixes 18)"
echo -e "Upstream version:   $(get_xorg_version libXfixes lib)"
echo -e "Ubuntu version:     $(get_ubuntu_version libxfixes ${1:-raring})"
